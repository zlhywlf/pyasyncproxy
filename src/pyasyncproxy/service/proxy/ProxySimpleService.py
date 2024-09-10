"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from typing import override

from pyasyncproxy.model.dto.ProxyAppContext import ProxyAppContext
from pyasyncproxy.model.dto.ProxyRequest import ProxyRequest
from pyasyncproxy.model.dto.ProxyRequestContext import ProxyRequestContext
from pyasyncproxy.model.dto.ProxyResponse import ProxyResponse
from pyasyncproxy.model.po.ProxyUrl import ProxyUrl
from pyasyncproxy.service.proxy.ProxyEngine import ProxyEngine
from pyasyncproxy.service.ProxyService import ProxyService


class ProxySimpleService(ProxyService):
    """default proxy service."""

    def __init__(self, app_ctx: ProxyAppContext, engine: ProxyEngine) -> None:
        """Init."""
        self._engine = engine
        self._app_ctx = app_ctx

    @override
    async def forward_request(self, request: ProxyRequest) -> ProxyResponse:
        ctx = ProxyRequestContext(request_id=self._app_ctx.request_id_factory(), data=request, app=self._app_ctx)
        return await self._engine.process(ctx)

    @override
    async def get_proxy_pool(self) -> list[ProxyUrl]:
        return await self._app_ctx.ip_pool.get_proxy_pool()

    @override
    async def add_proxy_url(self, url: ProxyUrl) -> None:
        await self._app_ctx.ip_pool.add_proxy_url(url)
