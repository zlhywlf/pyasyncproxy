"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from typing import override

from pyasyncproxy.cnst.ProxyCheckerEnum import ProxyCheckerEnum
from pyasyncproxy.model.dto.ProxyRequestContext import ProxyRequestContext
from pyasyncproxy.model.dto.ProxyRouteInfo import ProxyRouteChecker
from pyasyncproxy.service.proxy.ProxyNode import ProxyNode


class ProxyIpPoolNode(ProxyNode):
    """get static IP from the pool."""

    @override
    async def handle(self, ctx: ProxyRequestContext) -> ProxyRouteChecker:
        if ctx.proxy_url:
            return ProxyRouteChecker(curr_node_name=self.__class__.__name__, type=ProxyCheckerEnum.OK)
        proxy_url = await ctx.app.ip_pool.get_proxy_url()
        if not proxy_url:
            ctx.msg = "Proxy IP exhausted"
            return ProxyRouteChecker(curr_node_name=self.__class__.__name__, type=ProxyCheckerEnum.ERROR)
        ctx.proxy_url = proxy_url
        return ProxyRouteChecker(curr_node_name=self.__class__.__name__, type=ProxyCheckerEnum.OK)
