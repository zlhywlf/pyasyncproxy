"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from abc import ABC, abstractmethod

from pyasyncproxy.model.po.ProxyUrl import ProxyUrl


class ProxyIpPool(ABC):
    """proxy ip pool."""

    def __init__(self) -> None:
        """Init."""
        self._index = 0

    async def get_proxy_url(self) -> ProxyUrl | None:
        """Get proxy url."""
        curr = self._index % await self.get_proxy_pool_length()
        while True:
            url = await self.get_curr_proxy_url()
            self._index = (self._index + 1) % await self.get_proxy_pool_length()
            if url and url.is_alive:
                return url
            if self._index == curr:
                return None

    @abstractmethod
    async def add_proxy_url(self, proxy_url: ProxyUrl) -> None:
        """Add proxy url."""

    @abstractmethod
    async def get_proxy_pool(self) -> list[ProxyUrl]:
        """Get all proxy url from pool."""

    @abstractmethod
    async def get_curr_proxy_url(self) -> ProxyUrl | None:
        """Get current proxy url from pool."""

    @abstractmethod
    async def get_proxy_pool_length(self) -> int:
        """Get proxy pool length."""

    @property
    def index(self) -> int:
        """Current index of proxy pool."""
        return self._index

    @abstractmethod
    async def update_proxy_url(self, proxy_url: ProxyUrl) -> None:
        """Update proxy url."""
