"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from collections.abc import Mapping
from typing import override

from pyasyncproxy.model.dto.ProxyAppContext import ProxyAppContext
from pyasyncproxy.model.dto.ProxyRequest import ProxyRequest
from pyasyncproxy.model.dto.ProxyRequestContext import ProxyRequestContext
from pyasyncproxy.model.dto.ProxyResponse import ProxyResponse
from pyasyncproxy.service.proxy.ProxyEngine import ProxyEngine
from pyasyncproxy.service.ProxyService import ProxyService


class ProxySimpleService(ProxyService):
    """default proxy service."""

    def __init__(self, app_ctx: ProxyAppContext, engine: ProxyEngine) -> None:
        """Init."""
        self._engine = engine
        self._app_ctx = app_ctx

    @override
    async def forward_request(self, url: str, method: str, content: bytes, headers: Mapping[str, str]) -> ProxyResponse:
        request_id = self._app_ctx.snowflake.next_id()
        data = ProxyRequest(url=url, method=method, content=content, headers=headers)
        ctx = ProxyRequestContext(request_id=request_id, data=data, app=self._app_ctx)
        return await self._engine.process(ctx)
