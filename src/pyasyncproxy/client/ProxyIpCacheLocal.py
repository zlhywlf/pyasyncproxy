"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import logging
from collections.abc import Awaitable, Callable
from datetime import datetime, timedelta, timezone
from typing import Any, override

import anyio
from pydantic import BaseModel

from pyasyncproxy.client.ProxyIpCache import ProxyIpCache
from pyasyncproxy.model.po.ProxyUrl import ProxyUrl
from pyasyncproxy.model.po.ProxyUrlCache import ProxyUrlCache

logger = logging.getLogger(__name__)


class _CacheInfo(BaseModel):
    key: str
    expiry: float
    create_time: datetime


class ProxyIpCacheLocal(ProxyIpCache):
    """local proxy ip cache."""

    def __init__(self) -> None:
        """Init."""
        self._proxy_url_cache: dict[str, ProxyUrlCache] = {}

    @override
    async def get_proxy_url(self, business_id: str) -> ProxyUrl | None:
        cache = self._proxy_url_cache.get(business_id)
        logger.info(cache)
        return cache.url if cache else None

    @override
    async def set_proxy_url(self, business_id: str, proxy_url: ProxyUrl, expiry: float) -> None:
        now = datetime.now(tz=timezone(timedelta(hours=8)))
        self._proxy_url_cache[business_id] = ProxyUrlCache(
            url=proxy_url,
            expiry=expiry,
            business_id=business_id,
            create_time=now,
        )
        await self._background_task(
            self._del_cache, _CacheInfo(key=business_id, expiry=max(expiry, 0), create_time=now)
        )

    @override
    async def is_exist_proxy_url(self, business_id: str) -> bool:
        return business_id in self._proxy_url_cache

    async def _del_cache(self, cache_info: _CacheInfo) -> None:
        await anyio.sleep(cache_info.expiry)
        url = self._proxy_url_cache[cache_info.key]
        if url.create_time == cache_info.create_time:
            self._proxy_url_cache.pop(cache_info.key)
            logger.info(f"{url} has expired")

    @staticmethod
    async def _background_task(func: Callable[[_CacheInfo], Awaitable[Any]], cache_info: _CacheInfo) -> None:
        tg = anyio.create_task_group()
        await tg.__aenter__()
        tg.start_soon(func, cache_info)
