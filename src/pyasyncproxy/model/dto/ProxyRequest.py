"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from collections.abc import Mapping

from pydantic import BaseModel

from pyasyncproxy.model.po.ProxyUrl import ProxyUrl


class ProxyRequest(BaseModel):
    """Request parameters for the route of /proxy."""

    url: str
    headers: Mapping[str, str]
    method: str
    content: bytes
    retry: int = 3
    proxy_url: ProxyUrl | None = None
