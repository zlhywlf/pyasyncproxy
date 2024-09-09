"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from abc import ABC, abstractmethod

from pyasyncproxy.model.dto.ProxyRequest import ProxyRequest
from pyasyncproxy.model.dto.ProxyResponse import ProxyResponse
from pyasyncproxy.model.po.ProxyUrl import ProxyUrl


class ProxyService(ABC):
    """proxy service."""

    @abstractmethod
    async def forward_request(self, request: ProxyRequest) -> ProxyResponse:
        """Forward request."""

    @abstractmethod
    async def get_proxy_pool(self) -> list[ProxyUrl]:
        """Get all proxy url from pool."""

    @abstractmethod
    async def add_proxy_url(self, url: ProxyUrl) -> None:
        """Add proxy url."""
