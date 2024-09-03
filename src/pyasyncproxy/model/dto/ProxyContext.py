"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from pydantic import BaseModel

from pyasyncproxy.model.dto.ProxyRequest import ProxyRequest


class ProxyContext(BaseModel):
    """proxy context."""

    data: ProxyRequest
    msg: str | None = None
    proxy_url: str | None = None
