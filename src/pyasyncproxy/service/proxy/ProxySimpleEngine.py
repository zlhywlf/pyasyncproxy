"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import logging
from collections.abc import Mapping
from typing import override

from pyasyncproxy.client.CacheClient import CacheClient
from pyasyncproxy.client.DbClient import DbClient
from pyasyncproxy.env.ProjectEnv import ProjectEnv
from pyasyncproxy.model.dto.ProxyContext import ProxyContext
from pyasyncproxy.model.dto.ProxyRequest import ProxyRequest
from pyasyncproxy.model.dto.ProxyResponse import ProxyResponse
from pyasyncproxy.model.dto.ProxyRouteInfo import ProxyRouteChecker
from pyasyncproxy.model.dto.ProxyTree import ProxyNodeTree, ProxyRootTree
from pyasyncproxy.service.proxy.ProxyEngine import ProxyEngine
from pyasyncproxy.service.proxy.ProxyNode import ProxyNode

logger = logging.getLogger(__name__)


class ProxySimpleEngine(ProxyEngine):
    """default engine."""

    def __init__(
        self,
        proxy_tree: ProxyRootTree,
        node_map: Mapping[str, ProxyNode],
        env: ProjectEnv,
        cache_client: CacheClient,
        db_client: DbClient,
    ) -> None:
        """Init."""
        self._proxy_tree = proxy_tree
        self._node_map = node_map
        self._env = env
        self._cache_client = cache_client
        self._db_client = db_client

    @override
    async def process(self, data: ProxyRequest) -> ProxyResponse:
        node_name: str | None = self._proxy_tree.name
        response: ProxyResponse | None = None
        ctx = ProxyContext(data=data, env=self._env, cache_client=self._cache_client, db_client=self._db_client)
        while node_name:
            node = self._node_map[node_name]
            checker = await node.handle(ctx)
            response = checker.response
            logger.info(f"{ctx} {checker}")
            node_name = self._get_next_node(checker)
        if not response:
            msg = f"process failure for {self._proxy_tree} | {data}"
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
