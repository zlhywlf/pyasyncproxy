"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from typing import override

from pyasyncproxy.model.dto.ProxyRequest import ProxyRequest
from pyasyncproxy.model.dto.ProxyResponse import ProxyResponse
from pyasyncproxy.service.proxy.ProxyEngine import ProxyEngine
from pyasyncproxy.service.proxy.ProxyService import ProxyService


class ProxySimpleService(ProxyService):
    """default proxy service."""

    def __init__(self, engine: ProxyEngine) -> None:
        """Init."""
        self._engine = engine

    @override
    async def forward_request(self, request: ProxyRequest) -> ProxyResponse:
        return await self._engine.process(request)
