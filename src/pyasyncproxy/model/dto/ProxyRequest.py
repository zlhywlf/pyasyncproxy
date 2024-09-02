"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from collections.abc import Mapping

from pydantic import BaseModel


class ProxyRequest(BaseModel):
    """Request parameters for the route of /proxy."""

    request_id: int
    business_id: str | None = None
    url: str
    headers: Mapping[str, str]
    method: str
    content: bytes
    timeout: float = 200
