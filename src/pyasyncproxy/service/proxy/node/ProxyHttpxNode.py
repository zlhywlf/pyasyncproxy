"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from typing import override

import httpx

from pyasyncproxy.cnst.ProxyCheckerEnum import ProxyCheckerEnum
from pyasyncproxy.model.dto.ProxyRequestContext import ProxyRequestContext
from pyasyncproxy.model.dto.ProxyResponse import ProxyResponse
from pyasyncproxy.model.dto.ProxyRouteInfo import ProxyRouteChecker
from pyasyncproxy.service.proxy.ProxyNode import ProxyNode


class ProxyHttpxNode(ProxyNode):
    """Request target service."""

    @override
    async def handle(self, ctx: ProxyRequestContext) -> ProxyRouteChecker:
        if ctx.data.retry <= 0:
            ctx.msg = "Attempted multiple times but still failed"
            return ProxyRouteChecker(curr_node_name=self.__class__.__name__, type=ProxyCheckerEnum.ERROR)
        mounts = None
        if ctx.proxy_url and ctx.app.env.proxy_auth:
            auth = ctx.app.env.proxy_auth.get(ctx.proxy_url.category)
            auth = f"{auth}@" if auth else ""
            proxy_url = f"{ctx.proxy_url.protocol}://{auth}{ctx.proxy_url.ip}:{ctx.proxy_url.port}"
            mounts = {
                "http://": httpx.AsyncHTTPTransport(proxy=proxy_url),
                "https://": httpx.AsyncHTTPTransport(proxy=proxy_url),
            }
        try:
            async with (
                httpx.AsyncClient(mounts=mounts, timeout=httpx.Timeout(None)) as client,
                client.stream(
                    method=ctx.data.method, url=ctx.data.url, headers=ctx.data.headers, content=ctx.data.content
                ) as r,
            ):
                status_code = r.status_code
                if not ctx.data.proxy_url and ctx.proxy_url:
                    h_proxy_url = f"{ctx.app.env.project_name}:{ctx.proxy_url.model_dump_json()}"
                    r.headers[ctx.app.env.forward_url_key] = h_proxy_url
                headers = r.headers
                content = b"".join([chunk async for chunk in r.aiter_raw()])
        except (httpx.ReadTimeout, httpx.WriteTimeout) as e:
            ctx.msg = str(e)
            return ProxyRouteChecker(curr_node_name=self.__class__.__name__, type=ProxyCheckerEnum.ERROR)
        except (httpx.ConnectTimeout, httpx.ConnectError, httpx.ProxyError) as e:
            if ctx.proxy_url:
                ctx.proxy_url.is_alive = False
                await ctx.app.ip_pool.update_proxy_url(ctx.proxy_url)
            if not ctx.data.proxy_url:
                ctx.data.retry -= 1
                ctx.proxy_url = None
                return ProxyRouteChecker(curr_node_name=self.__class__.__name__, type=ProxyCheckerEnum.OVER)
            ctx.msg = str(e)
            return ProxyRouteChecker(curr_node_name=self.__class__.__name__, type=ProxyCheckerEnum.ERROR)
        return ProxyRouteChecker(
            curr_node_name=self.__class__.__name__,
            type=ProxyCheckerEnum.OK,
            response=ProxyResponse(
                content=content,
                code=status_code,
                headers=headers,
                media_type=headers.get("content-type"),
            ),
        )
