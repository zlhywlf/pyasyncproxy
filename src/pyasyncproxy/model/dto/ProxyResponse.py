"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from collections.abc import Mapping

from pydantic import BaseModel


class ProxyResponse(BaseModel):
    """Response for the route of /proxy."""

    code: int
    headers: Mapping[str, str]
    media_type: str
    content: bytes
