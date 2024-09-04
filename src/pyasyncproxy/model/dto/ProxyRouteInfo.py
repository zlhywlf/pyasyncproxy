"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from pydantic import BaseModel

from pyasyncproxy.cnst.ProxyCheckerEnum import ProxyCheckerEnum
from pyasyncproxy.model.dto.ProxyResponse import ProxyResponse


class ProxyRouteType(BaseModel):
    """route type."""

    type: ProxyCheckerEnum


class ProxyRouteInfo(ProxyRouteType):
    """route info."""

    next_node_name: str | None = None


class ProxyRouteChecker(ProxyRouteInfo):
    """route type checker."""

    curr_node_name: str
    response: ProxyResponse | None = None
