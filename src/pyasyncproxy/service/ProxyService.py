"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from abc import ABC, abstractmethod

from pyasyncproxy.model.dto.ProxyContext import ProxyContext
from pyasyncproxy.model.dto.ProxyResponse import ProxyResponse


class ProxyService(ABC):
    """proxy service."""

    @abstractmethod
    async def forward_request(self, ctx: ProxyContext) -> ProxyResponse:
        """Forward request."""
