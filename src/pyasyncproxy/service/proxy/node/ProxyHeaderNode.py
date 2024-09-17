"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from typing import override

from pyasyncproxy.cnst.ProxyCheckerEnum import ProxyCheckerEnum
from pyasyncproxy.model.dto.ProxyRequestContext import ProxyRequestContext
from pyasyncproxy.model.dto.ProxyRouteInfo import ProxyRouteChecker
from pyasyncproxy.service.proxy.ProxyNode import ProxyNode


class ProxyHeaderNode(ProxyNode):
    """handle headers."""

    @override
    async def handle(self, ctx: ProxyRequestContext) -> ProxyRouteChecker:
        data = ctx.data
        data.url = data.headers.get(ctx.app.env.forward_url_key) or data.url
        retry = data.headers.get(ctx.app.env.forward_retry_key)
        if retry and not retry.isdigit():
            ctx.msg = f"{ctx.app.env.forward_retry_key} must be digit"
            return ProxyRouteChecker(curr_node_name=self.__class__.__name__, type=ProxyCheckerEnum.ERROR)
        data.retry = int(retry) if retry else data.retry
        data.headers = {k: v for k, v in data.headers.items() if k not in (ctx.app.env.exclude_headers or [])}
        if data.proxy_url:
            ctx.proxy_url = data.proxy_url
            return ProxyRouteChecker(curr_node_name=self.__class__.__name__, type=ProxyCheckerEnum.OK)
        return ProxyRouteChecker(curr_node_name=self.__class__.__name__, type=ProxyCheckerEnum.OVER)
