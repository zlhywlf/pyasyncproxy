"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from abc import ABC, abstractmethod

from pyasyncproxy.model.dto.ProxyRequestContext import ProxyRequestContext
from pyasyncproxy.model.dto.ProxyRouteInfo import ProxyRouteChecker


class ProxyNode(ABC):
    """Proxy execution node."""

    @abstractmethod
    async def handle(self, ctx: ProxyRequestContext) -> ProxyRouteChecker:
        """Handle."""
