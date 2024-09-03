"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from collections.abc import Mapping
from typing import override

import pyasyncproxy.service.proxy.node
from pyasyncproxy.common.ModuleUtil import get_modules
from pyasyncproxy.service.proxy.ProxyNode import ProxyNode
from pyasyncproxy.service.proxy.ProxyNodeFactory import ProxyNodeFactory


class ProxySimpleNodeFactory(ProxyNodeFactory):
    """Proxy execution node factory."""

    @override
    def collect_nodes(self) -> Mapping[str, ProxyNode]:
        """Collect nodes."""
        modules = get_modules(pyasyncproxy.service.proxy.node.__name__)
        nodes_map = {}
        for module in modules:
            if not module:
                continue
            for obj in module.__dict__.values():
                if isinstance(obj, type) and obj is not ProxyNode and issubclass(obj, ProxyNode):
                    nodes_map[obj.__name__] = obj()
        return nodes_map
