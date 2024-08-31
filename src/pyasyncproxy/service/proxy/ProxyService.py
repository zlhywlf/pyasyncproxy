"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from abc import ABC, abstractmethod

from pyasyncproxy.model.dto.ProxyRequest import ProxyRequest
from pyasyncproxy.model.dto.ProxyResponse import ProxyResponse


class ProxyService(ABC):
    """proxy service."""

    @abstractmethod
    async def forward_request(self, request: ProxyRequest) -> ProxyResponse:
        """Forward request."""
