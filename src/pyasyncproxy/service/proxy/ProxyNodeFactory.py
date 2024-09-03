"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from abc import ABC, abstractmethod
from collections.abc import Mapping

from pyasyncproxy.service.proxy.ProxyNode import ProxyNode


class ProxyNodeFactory(ABC):
    """Proxy execution node factory."""

    @abstractmethod
    def collect_nodes(self) -> Mapping[str, ProxyNode]:
        """Collect nodes."""
