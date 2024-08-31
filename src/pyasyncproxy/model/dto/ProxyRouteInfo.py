"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from pydantic import BaseModel

from pyasyncproxy.model.dto.ProxyResponse import ProxyResponse


class ProxyRouteType(BaseModel):
    """route type."""

    type: str


class ProxyRouteInfo(ProxyRouteType):
    """route info."""

    next_node_name: str


class ProxyRouteChecker(ProxyRouteType):
    """route type checker."""

    curr_node_name: str
    response: ProxyResponse
