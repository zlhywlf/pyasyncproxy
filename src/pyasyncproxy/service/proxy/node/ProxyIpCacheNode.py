"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from typing import override

from pyasyncproxy.cnst.ProxyCheckerEnum import ProxyCheckerEnum
from pyasyncproxy.model.dto.ProxyRequestContext import ProxyRequestContext
from pyasyncproxy.model.dto.ProxyRouteInfo import ProxyRouteChecker
from pyasyncproxy.service.proxy.ProxyNode import ProxyNode


class ProxyIpCacheNode(ProxyNode):
    """get IP from the cache and save IP to the cache."""

    @override
    async def handle(self, ctx: ProxyRequestContext) -> ProxyRouteChecker:
        business_id = ctx.data.business_id or str(ctx.request_id)
        if not ctx.proxy_url:
            proxy_url = await ctx.app.ip_cache.get_proxy_url(business_id)
            if not proxy_url:
                ctx.msg = f"{business_id}: Proxy not found in the cache"
                return ProxyRouteChecker(curr_node_name=self.__class__.__name__, type=ProxyCheckerEnum.ERROR)
            ctx.proxy_url = proxy_url
        await ctx.app.ip_cache.set_proxy_url(business_id, ctx.proxy_url, ctx.data.expiry)
        return ProxyRouteChecker(curr_node_name=self.__class__.__name__, type=ProxyCheckerEnum.OK)
