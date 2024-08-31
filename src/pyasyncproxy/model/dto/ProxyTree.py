"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from pydantic import BaseModel

from pyasyncproxy.model.dto.ProxyRouteInfo import ProxyRouteInfo


class ProxyNodeTree(BaseModel):
    """sub node."""

    name: str
    next_name: str | None = None
    routes: list[ProxyRouteInfo] | None = None


class ProxyRootTree(ProxyNodeTree):
    """root node."""

    nodes: list[ProxyNodeTree] | None = None
