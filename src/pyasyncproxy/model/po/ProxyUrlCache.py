"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from datetime import datetime

from pydantic import BaseModel

from pyasyncproxy.model.po.ProxyUrl import ProxyUrl


class ProxyUrlCache(BaseModel):
    """proxy url cache."""

    url: ProxyUrl | None
    expiry: float
    business_id: str
    create_time: datetime
