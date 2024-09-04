"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from typing import override

from pyasyncproxy.cnst.ProxyCheckerEnum import ProxyCheckerEnum
from pyasyncproxy.model.dto.ProxyContext import ProxyContext
from pyasyncproxy.model.dto.ProxyRouteInfo import ProxyRouteChecker
from pyasyncproxy.service.proxy.ProxyNode import ProxyNode


class ProxyHeaderNode(ProxyNode):
    """handle headers."""

    @override
    async def handle(self, ctx: ProxyContext) -> ProxyRouteChecker:
        data = ctx.data
        url = data.headers.get(ctx.env.forward_url_key)
        method = data.headers.get(ctx.env.forward_method_key)
        if not url or not method:
            ctx.msg = f"{ctx.env.forward_url_key} and {ctx.env.forward_method_key} must be in headers"
            return ProxyRouteChecker(curr_node_name=self.__class__.__name__, type=ProxyCheckerEnum.ERROR)
        timeout = data.headers.get(ctx.env.forward_timeout)
        if timeout and not timeout.isnumeric():
            ctx.msg = f"{ctx.env.forward_timeout} must be numeric"
            return ProxyRouteChecker(curr_node_name=self.__class__.__name__, type=ProxyCheckerEnum.ERROR)
        expiry = data.headers.get(ctx.env.business_expiry_key)
        if expiry and not expiry.isnumeric():
            ctx.msg = f"{ctx.env.business_expiry_key} must be numeric"
            return ProxyRouteChecker(curr_node_name=self.__class__.__name__, type=ProxyCheckerEnum.ERROR)
        retry = data.headers.get(ctx.env.forward_retry_key)
        if retry and not retry.isdigit():
            ctx.msg = f"{ctx.env.forward_retry_key} must be digit"
            return ProxyRouteChecker(curr_node_name=self.__class__.__name__, type=ProxyCheckerEnum.ERROR)
        data.business_id = data.headers.get(ctx.env.business_id_key)
        data.expiry = float(expiry) if expiry else data.expiry
        data.timeout = float(timeout) if timeout else data.timeout
        data.retry = int(retry) if retry else data.retry
        data.url = url
        data.method = method
        data.headers = {k: v for k, v in data.headers.items() if k not in (ctx.env.exclude_headers or [])}
        if not data.business_id:
            return ProxyRouteChecker(curr_node_name=self.__class__.__name__, type=ProxyCheckerEnum.OVER)
        return ProxyRouteChecker(curr_node_name=self.__class__.__name__, type=ProxyCheckerEnum.OK)
