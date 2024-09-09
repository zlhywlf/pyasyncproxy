"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from typing import override

from pyasyncproxy.cnst.ProxyCheckerEnum import ProxyCheckerEnum
from pyasyncproxy.model.dto.ProxyContext import ProxyContext
from pyasyncproxy.model.dto.ProxyRouteInfo import ProxyRouteChecker
from pyasyncproxy.service.proxy.ProxyNode import ProxyNode


class ProxyStaticIpNode(ProxyNode):
    """get static IP from the pool."""

    @override
    async def handle(self, ctx: ProxyContext) -> ProxyRouteChecker:
        if not ctx.first:
            return ProxyRouteChecker(curr_node_name=self.__class__.__name__, type=ProxyCheckerEnum.CACHE)
        proxy_url = await ctx.dynamic_ip_pool.get_proxy_url()
        if not proxy_url:
            return ProxyRouteChecker(curr_node_name=self.__class__.__name__, type=ProxyCheckerEnum.OVER)
        ctx.proxy_url = proxy_url
        return ProxyRouteChecker(curr_node_name=self.__class__.__name__, type=ProxyCheckerEnum.CACHE)
