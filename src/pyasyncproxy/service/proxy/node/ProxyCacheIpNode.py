"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from typing import override

from pyasyncproxy.cnst.ProxyCheckerEnum import ProxyCheckerEnum
from pyasyncproxy.model.dto.ProxyContext import ProxyContext
from pyasyncproxy.model.dto.ProxyRouteInfo import ProxyRouteChecker
from pyasyncproxy.service.proxy.ProxyNode import ProxyNode


class ProxyCacheIpNode(ProxyNode):
    """Retrieve IP from cache."""

    @override
    async def handle(self, ctx: ProxyContext) -> ProxyRouteChecker:
        business_id = ctx.data.business_id or str(ctx.request_id)
        proxy_url = await ctx.cache_client.get_proxy_url(business_id) if not ctx.first else None
        if not proxy_url:
            ctx.first = True
            proxy_url = await ctx.db_client.get_proxy_url()
            if not proxy_url:
                ctx.msg = "Proxy IP exhausted"
                return ProxyRouteChecker(curr_node_name=self.__class__.__name__, type=ProxyCheckerEnum.ERROR)
            await ctx.cache_client.set_proxy_url(business_id, proxy_url, ctx.data.expiry)
        ctx.proxy_url = proxy_url
        return ProxyRouteChecker(curr_node_name=self.__class__.__name__, type=ProxyCheckerEnum.OK)
