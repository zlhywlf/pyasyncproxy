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
        mounts = (
            {
                "http://": httpx.AsyncHTTPTransport(proxy=ctx.proxy_url),
                "https://": httpx.AsyncHTTPTransport(proxy=ctx.proxy_url),
            }
            if ctx.proxy_url
            else None
        )
        async with httpx.AsyncClient(mounts=mounts) as client:
            res = await client.request(
                method=ctx.data.method,
                url=ctx.data.url,
                headers=ctx.data.headers,
                content=ctx.data.content,
                timeout=httpx.Timeout(timeout=ctx.data.timeout),
            )
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
