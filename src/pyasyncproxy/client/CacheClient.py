"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from abc import ABC, abstractmethod

from pyasyncproxy.model.po.ProxyUrl import ProxyUrl


class CacheClient(ABC):
    """cache client."""

    @abstractmethod
    async def get_proxy_url(self, business_id: str) -> ProxyUrl | None:
        """Get proxy url."""

    @abstractmethod
    async def set_proxy_url(self, business_id: str, proxy_url: ProxyUrl, expiry: float) -> None:
        """Set proxy url."""
