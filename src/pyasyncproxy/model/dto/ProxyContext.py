"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from pydantic import BaseModel, Field

from pyasyncproxy.context.ProxyIpCache import ProxyIpCache
from pyasyncproxy.context.ProxyIpPool import ProxyIpPool
from pyasyncproxy.model.dto.ProjectEnv import ProjectEnv
from pyasyncproxy.model.dto.ProxyRequest import ProxyRequest
from pyasyncproxy.model.po.ProxyUrl import ProxyUrl


class ProxyContext(BaseModel, arbitrary_types_allowed=True):
    """proxy context."""

    request_id: int
    data: ProxyRequest
    env: ProjectEnv = Field(..., repr=False)
    ip_cache: ProxyIpCache = Field(..., repr=False)
    ip_pool: ProxyIpPool = Field(..., repr=False)
    msg: str | None = None
    proxy_url: ProxyUrl | None = None
    first: bool = False
