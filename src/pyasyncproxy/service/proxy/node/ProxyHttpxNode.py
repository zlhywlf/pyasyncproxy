"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from typing import override

import httpx

from pyasyncproxy.cnst.ProxyCheckerEnum import ProxyCheckerEnum
from pyasyncproxy.model.dto.ProxyContext import ProxyContext
from pyasyncproxy.model.dto.ProxyResponse import ProxyResponse
from pyasyncproxy.model.dto.ProxyRouteInfo import ProxyRouteChecker
from pyasyncproxy.service.proxy.ProxyNode import ProxyNode


class ProxyHttpxNode(ProxyNode):
    """Request target service."""

    @override
    async def handle(self, ctx: ProxyContext) -> ProxyRouteChecker:
        if ctx.data.retry <= 0:
            ctx.msg = "Attempted multiple times but still failed"
            return ProxyRouteChecker(curr_node_name=self.__class__.__name__, type=ProxyCheckerEnum.ERROR)
        mounts = None
        if ctx.proxy_url and ctx.env.proxy_auth:
            auth = ctx.env.proxy_auth.get(ctx.proxy_url.category)
            auth = f"{auth}@" if auth else ""
            proxy_url = f"{ctx.proxy_url.protocol}://{auth}{ctx.proxy_url.ip}:{ctx.proxy_url.port}"
            mounts = {
                "http://": httpx.AsyncHTTPTransport(proxy=proxy_url),
                "https://": httpx.AsyncHTTPTransport(proxy=proxy_url),
            }
        try:
            async with httpx.AsyncClient(mounts=mounts, timeout=httpx.Timeout(timeout=ctx.data.timeout)) as client:
                res = await client.request(
                    method=ctx.data.method,
                    url=ctx.data.url,
                    headers=ctx.data.headers,
                    content=ctx.data.content,
                )
        except httpx.ConnectTimeout:
            ctx.msg = "ConnectTimeout"
            return ProxyRouteChecker(curr_node_name=self.__class__.__name__, type=ProxyCheckerEnum.ERROR)
        except httpx.ConnectError:
            ctx.data.retry -= 1
            return ProxyRouteChecker(curr_node_name=self.__class__.__name__, type=ProxyCheckerEnum.OVER)
        return ProxyRouteChecker(
            curr_node_name=self.__class__.__name__,
            type=ProxyCheckerEnum.OK,
            response=ProxyResponse(
                content=res.content,
                code=res.status_code,
                headers=res.headers,
                media_type=res.headers.get("content-type"),
            ),
        )
