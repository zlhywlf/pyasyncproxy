"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from pydantic import BaseModel


class ProxyUrl(BaseModel):
    """proxy url."""

    index: int
    category: str
    protocol: str
    ip: str
    port: int
    adr: str | None
    is_alive: bool
