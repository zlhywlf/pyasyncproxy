"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from abc import ABC, abstractmethod

from pyasyncproxy.model.dto.ProxyRequest import ProxyRequest
from pyasyncproxy.model.dto.ProxyResponse import ProxyResponse


class ProxyEngine(ABC):
    """proxy service engine."""

    @abstractmethod
    async def process(self, data: ProxyRequest) -> ProxyResponse:
        """Process."""
