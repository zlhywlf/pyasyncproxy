"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from abc import ABC, abstractmethod

from pyasyncproxy.model.dto.ProxyTree import ProxyRootTree
from pyasyncproxy.service.proxy.ProxyEngine import ProxyEngine


class ProxyEngineFactory(ABC):
    """proxy service engine factory."""

    @abstractmethod
    def create_engine(self, proxy_tree: ProxyRootTree) -> ProxyEngine:
        """Create engine."""
