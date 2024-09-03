"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import logging
from datetime import datetime, timedelta, timezone
from typing import Any, override

import anyio
from pydantic import BaseModel

from pyasyncproxy.client.CacheClient import CacheClient
from pyasyncproxy.model.po.ProxyUrl import ProxyUrl
from pyasyncproxy.model.po.ProxyUrlCache import ProxyUrlCache

logger = logging.getLogger(__name__)


class _CacheInfo(BaseModel):
    cache_map: dict[str, Any]
    key: str
    expiry: float


async def _background_task(cache_info: _CacheInfo) -> None:
    async def _del_cache(cache_info: _CacheInfo) -> None:
        await anyio.sleep(cache_info.expiry)
        value = cache_info.cache_map.pop(cache_info.key)
        logger.info(f"{value} has expired")

    tg = anyio.create_task_group()
    await tg.__aenter__()
    tg.start_soon(_del_cache, cache_info)


class LocalCacheClient(CacheClient):
    """Local cache client."""

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
        self._proxy_url_cache[business_id] = ProxyUrlCache(
            url=proxy_url,
            expiry=expiry,
            business_id=business_id,
            create_time=datetime.now(tz=timezone(timedelta(hours=8))),
        )
        await _background_task(_CacheInfo(cache_map=self._proxy_url_cache, key=business_id, expiry=max(expiry, 0)))
