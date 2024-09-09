"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import logging
import pathlib
from typing import override

from pyasyncproxy.client.ProxyIpPool import ProxyIpPool
from pyasyncproxy.model.po.ProxyUrl import ProxyUrl

logger = logging.getLogger(__name__)


class ProxyIpPoolLocal(ProxyIpPool):
    """local proxy ip pool."""

    def __init__(self) -> None:
        """Init."""
        self._index = 0
        self._pool: list[ProxyUrl] = []
        data_path = pathlib.Path.cwd() / "ip.csv"
        with data_path.open("r") as f:
            for line in f.readlines():
                row = line.split(",")
                self._pool.append(
                    ProxyUrl(
                        category=row[0],
                        protocol=row[1],
                        ip=row[2],
                        port=int(row[3]),
                        adr=row[4],
                        is_alive=bool(row[5]),
                    )
                )

    @override
    async def get_proxy_url(self) -> ProxyUrl | None:
        url = self._pool[self._index]
        self._index = (self._index + 1) % len(self._pool)
        return url if url.is_alive else await self.get_proxy_url()

    @override
    async def add_proxy_url(self, proxy_url: ProxyUrl) -> None:
        self._pool.append(proxy_url)
        logger.info(proxy_url)
