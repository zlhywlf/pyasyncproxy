"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from typing import override

from pyasyncproxy.client.HttpClient import HttpClient
from pyasyncproxy.cnst.ProxyCheckerEnum import ProxyCheckerEnum
from pyasyncproxy.model.dto.ProxyContext import ProxyContext
from pyasyncproxy.model.dto.ProxyRouteInfo import ProxyRouteChecker
from pyasyncproxy.service.proxy.ProxyNode import ProxyNode


class ProxyHttpNode(ProxyNode):
    """Request target service."""

    def __init__(self, client_clazz: type[HttpClient]) -> None:
        """Init."""
        self._client_clazz = client_clazz

    @override
    async def handle(self, ctx: ProxyContext) -> ProxyRouteChecker:
        async with self._client_clazz() as client:
            res = await client.request(ctx.data)
        return ProxyRouteChecker(curr_node_name=self.__class__.__name__, type=ProxyCheckerEnum.OK, response=res)
