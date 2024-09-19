"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from pydantic import BaseModel, Field


class ProxyResponse(BaseModel):
    """Response for the route of proxy."""

    code: int
    headers: list[tuple[bytes, bytes]] | None = None
    media_type: str | None
    content: bytes = Field(..., repr=False)
