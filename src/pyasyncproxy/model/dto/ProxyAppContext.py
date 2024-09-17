"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from collections.abc import Callable
from dataclasses import dataclass

from pyasyncproxy.context.ProxyIpPool import ProxyIpPool
from pyasyncproxy.model.dto.ProjectEnv import ProjectEnv


@dataclass(frozen=True)
class ProxyAppContext:
    """proxy app context."""

    env: ProjectEnv
    ip_pool: ProxyIpPool
    request_id_factory: Callable[..., int]
