"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from abc import ABC, abstractmethod
from collections.abc import Mapping

from pyasyncproxy.model.dto.ProxyResponse import ProxyResponse


class ProxyService(ABC):
    """proxy service."""

    @abstractmethod
    async def forward_request(self, url: str, method: str, content: bytes, headers: Mapping[str, str]) -> ProxyResponse:
        """Forward request."""
