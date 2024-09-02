"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from typing import override

from pyasyncproxy.cnst.ProxyCheckerEnum import ProxyCheckerEnum
from pyasyncproxy.env.ProjectEnv import ProjectEnv
from pyasyncproxy.model.dto.ProxyContext import ProxyContext
from pyasyncproxy.model.dto.ProxyRouteInfo import ProxyRouteChecker
from pyasyncproxy.service.proxy.ProxyNode import ProxyNode


class ProxyHeaderNode(ProxyNode):
    """handle headers."""

    def __init__(self, env: ProjectEnv) -> None:
        """Init."""
        self._env = env

    @override
    async def handle(self, ctx: ProxyContext) -> ProxyRouteChecker:
        data = ctx.data
        url = data.headers.get(self._env.forward_url_key)
        method = data.headers.get(self._env.forward_method_key)
        if not url or not method:
            ctx.msg = f"{self._env.forward_url_key} and {self._env.forward_method_key} must be in headers"
            return ProxyRouteChecker(curr_node_name=self.__class__.__name__, type=ProxyCheckerEnum.ERROR)
        data.url = url
        data.method = method
        data.headers = {k: v for k, v in data.headers.items() if k not in (self._env.exclude_headers or [])}
        return ProxyRouteChecker(curr_node_name=self.__class__.__name__, type=ProxyCheckerEnum.OK)
