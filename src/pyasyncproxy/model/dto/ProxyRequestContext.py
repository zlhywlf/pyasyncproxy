"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from pydantic import BaseModel, Field

from pyasyncproxy.model.dto.ProxyAppContext import ProxyAppContext
from pyasyncproxy.model.dto.ProxyRequest import ProxyRequest
from pyasyncproxy.model.po.ProxyUrl import ProxyUrl


class ProxyRequestContext(BaseModel, arbitrary_types_allowed=True):
    """proxy request context."""

    request_id: int
    data: ProxyRequest
    app: ProxyAppContext = Field(..., repr=False)
    msg: str | None = None
    proxy_url: ProxyUrl | None = None
