"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import logging
from collections.abc import Mapping
from typing import override

from pyasyncproxy.model.dto.ProxyContext import ProxyContext
from pyasyncproxy.model.dto.ProxyResponse import ProxyResponse
from pyasyncproxy.model.dto.ProxyRouteInfo import ProxyRouteChecker
from pyasyncproxy.model.dto.ProxyTree import ProxyNodeTree, ProxyRootTree
from pyasyncproxy.service.proxy.ProxyEngine import ProxyEngine
from pyasyncproxy.service.proxy.ProxyNode import ProxyNode

logger = logging.getLogger(__name__)


class ProxySimpleEngine(ProxyEngine):
    """default engine."""

    def __init__(self, proxy_tree: ProxyRootTree, node_map: Mapping[str, ProxyNode]) -> None:
        """Init."""
        self._proxy_tree = proxy_tree
        self._node_map = node_map

    @override
    async def process(self, ctx: ProxyContext) -> ProxyResponse:
        node_name: str | None = self._proxy_tree.name
        response: ProxyResponse | None = None
        while node_name:
            node = self._node_map[node_name]
            checker = await node.handle(ctx)
            response = checker.response
            logger.info(f"{ctx} {checker}")
            node_name = self._get_next_node(checker)
        if not response:
            msg = f"process failure for {self._proxy_tree} | {ctx.data}"
            raise RuntimeError(msg)
        return response

    def _get_next_node(self, checker: ProxyRouteChecker) -> str | None:
        if not self._proxy_tree.nodes:
            return None
        for node in self._proxy_tree.nodes:
            if self._decide(node, checker):
                return node.next_name
        return None

    @staticmethod
    def _decide(node: ProxyNodeTree, checker: ProxyRouteChecker) -> bool:
        if node.name != checker.curr_node_name or not node.routes:
            return False
        for route in node.routes:
            if route.type == checker.type:
                node.next_name = route.next_node_name
                return True
        return False
