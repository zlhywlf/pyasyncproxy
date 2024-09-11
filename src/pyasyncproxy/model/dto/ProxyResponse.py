"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from collections.abc import Mapping

from pydantic import BaseModel, Field


class ProxyResponse(BaseModel):
    """Response for the route of proxy."""

    code: int
    headers: Mapping[str, str] | None = None
    media_type: str | None
    content: bytes = Field(..., repr=False)
