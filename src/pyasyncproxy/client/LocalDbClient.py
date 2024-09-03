"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import logging
import pathlib
from typing import override

from pyasyncproxy.client.DbClient import DbClient
from pyasyncproxy.model.po.ProxyUrl import ProxyUrl

logger = logging.getLogger(__name__)


class LocalDbClient(DbClient):
    """local database client."""

    def __init__(self) -> None:
        """Init."""
        self._index = -1
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
        self._len = len(self._pool)

    @override
    async def get_proxy_url(self) -> ProxyUrl | None:
        if self._index == self._len:
            self._index = -1
        self._index += 1
        return self._pool[self._index]

    @override
    async def add_proxy_url(self, proxy_url: ProxyUrl) -> None:
        self._pool.append(proxy_url)
        logger.info(proxy_url)
        self._len = len(self._pool)
