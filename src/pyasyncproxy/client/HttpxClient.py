"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import logging
from types import TracebackType
from typing import Self, override

import httpx

from pyasyncproxy.client.HttpClient import HttpClient
from pyasyncproxy.model.dto.ProxyRequest import ProxyRequest
from pyasyncproxy.model.dto.ProxyResponse import ProxyResponse

logger = logging.getLogger(__name__)


class HttpxClient(HttpClient):
    """httpx client."""

    def __init__(self, proxy_url: str | None = None) -> None:
        """Init."""
        self._mounts = (
            {
                "http://": httpx.AsyncHTTPTransport(proxy=proxy_url),
                "https://": httpx.AsyncHTTPTransport(proxy=proxy_url),
            }
            if proxy_url
            else None
        )
        self._client: httpx.AsyncClient | None = None

    @override
    async def request(self, req: ProxyRequest) -> ProxyResponse:
        if not self._client:
            msg = "No HTTP client"
            raise RuntimeError(msg)
        res = await self._client.request(
            method=req.method,
            url=req.url,
            headers=req.headers,
            content=req.content,
            timeout=httpx.Timeout(timeout=req.timeout),
        )
        logger.info(f"response is {res}")
        return ProxyResponse(
            content=res.content,
            code=res.status_code,
            headers=res.headers,
            media_type=res.headers.get("content-type"),
        )

    @override
    async def __aenter__(self) -> Self:
        timeout = httpx.Timeout(timeout=200)
        self._client = await httpx.AsyncClient(mounts=self._mounts, timeout=timeout).__aenter__()
        return self

    @override
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None = None,
        exc_val: BaseException | None = None,
        exc_tb: TracebackType | None = None,
    ) -> None:
        if self._client:
            await self._client.__aexit__(exc_type, exc_val, exc_tb)
