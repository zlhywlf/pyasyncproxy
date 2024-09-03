"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from typing import override

from pyasyncproxy.model.dto.ProxyContext import ProxyContext
from pyasyncproxy.model.dto.ProxyResponse import ProxyResponse
from pyasyncproxy.service.proxy.ProxyEngine import ProxyEngine
from pyasyncproxy.service.ProxyService import ProxyService


class ProxySimpleService(ProxyService):
    """default proxy service."""

    def __init__(self, engine: ProxyEngine) -> None:
        """Init."""
        self._engine = engine

    @override
    async def forward_request(self, ctx: ProxyContext) -> ProxyResponse:
        return await self._engine.process(ctx)
