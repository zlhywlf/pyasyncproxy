"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from dataclasses import dataclass

from pyasyncproxy.common.Snowflake import Snowflake
from pyasyncproxy.context.ProxyIpCache import ProxyIpCache
from pyasyncproxy.context.ProxyIpPool import ProxyIpPool
from pyasyncproxy.model.dto.ProjectEnv import ProjectEnv


@dataclass(frozen=True)
class ProxyAppContext:
    """proxy app context."""

    env: ProjectEnv
    ip_cache: ProxyIpCache
    ip_pool: ProxyIpPool
    snowflake: Snowflake
