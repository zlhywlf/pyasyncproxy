"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from abc import ABC, abstractmethod

from pyasyncproxy.model.po.ProxyUrl import ProxyUrl


class DbClient(ABC):
    """database client."""

    @abstractmethod
    async def get_proxy_url(self) -> ProxyUrl | None:
        """Get proxy url."""

    @abstractmethod
    async def add_proxy_url(self, proxy_url: ProxyUrl) -> None:
        """Add proxy url."""
