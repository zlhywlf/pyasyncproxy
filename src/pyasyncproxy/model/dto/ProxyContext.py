"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from pydantic import BaseModel, Field

from pyasyncproxy.client.CacheClient import CacheClient
from pyasyncproxy.client.DynamicIpPool import DynamicIpPool
from pyasyncproxy.model.dto.ProjectEnv import ProjectEnv
from pyasyncproxy.model.dto.ProxyRequest import ProxyRequest
from pyasyncproxy.model.po.ProxyUrl import ProxyUrl


class ProxyContext(BaseModel, arbitrary_types_allowed=True):
    """proxy context."""

    request_id: int
    data: ProxyRequest
    env: ProjectEnv = Field(..., repr=False)
    cache_client: CacheClient = Field(..., repr=False)
    dynamic_ip_pool: DynamicIpPool = Field(..., repr=False)
    msg: str | None = None
    proxy_url: ProxyUrl | None = None
    first: bool = False
