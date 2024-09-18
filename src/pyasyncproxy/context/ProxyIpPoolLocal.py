"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import logging
import pathlib
from typing import override

from pyasyncproxy.context.ProxyIpPool import ProxyIpPool
from pyasyncproxy.model.po.ProxyUrl import ProxyUrl

logger = logging.getLogger(__name__)


class ProxyIpPoolLocal(ProxyIpPool):
    """local proxy ip pool."""

    def __init__(self) -> None:
        """Init."""
        super().__init__()
        self._pool: dict[int, ProxyUrl] = {}
        self._id_counter = 0
        data_path = pathlib.Path.cwd() / "ip.csv"
        if not data_path.exists():
            logger.warning(f"{data_path} not found")
            return
        with data_path.open("r") as f:
            for line in f.readlines():
                row = line.split(",")
                proxy_url = ProxyUrl(
                    index=self._id_counter,
                    category=row[0],
                    protocol=row[1],
                    ip=row[2],
                    port=int(row[3]),
                    adr=row[4],
                    is_alive=bool(row[5]),
                )
                self._pool[self._id_counter] = proxy_url
                self._id_counter += 1

    @override
    async def add_proxy_url(self, proxy_url: ProxyUrl) -> None:
        proxy_url.index = self._id_counter
        self._pool[self._id_counter] = proxy_url
        self._id_counter += 1
        logger.info(proxy_url)

    @override
    async def get_proxy_pool(self) -> list[ProxyUrl]:
        return list(self._pool.values())

    @override
    async def get_curr_proxy_url(self) -> ProxyUrl | None:
        return self._pool.get(self.index)

    @override
    async def get_proxy_pool_length(self) -> int:
        return len(self._pool)

    @override
    async def update_proxy_url(self, proxy_url: ProxyUrl) -> None:
        self._pool[proxy_url.index] = proxy_url
