"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from collections.abc import Mapping
from typing import override

from pyasyncproxy.env.ProjectEnv import ProjectEnv
from pyasyncproxy.model.dto.ProxyTree import ProxyRootTree
from pyasyncproxy.service.proxy.ProxyEngine import ProxyEngine
from pyasyncproxy.service.proxy.ProxyEngineFactory import ProxyEngineFactory
from pyasyncproxy.service.proxy.ProxyNode import ProxyNode
from pyasyncproxy.service.proxy.ProxySimpleEngine import ProxySimpleEngine


class ProxySimpleEngineFactory(ProxyEngineFactory):
    """proxy service engine factory."""

    def __init__(self, node_map: Mapping[str, ProxyNode], env: ProjectEnv) -> None:
        """Init."""
        self._node_map = node_map
        self._env = env

    @override
    def create_engine(self, proxy_tree: ProxyRootTree) -> ProxyEngine:
        return ProxySimpleEngine(proxy_tree, self._node_map, self._env)
