"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import logging
from collections.abc import Mapping

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Route

from pyasyncproxy.client.HttpxClient import HttpxClient
from pyasyncproxy.env.ProjectEnv import ProjectEnv
from pyasyncproxy.model.dto.ProxyRequest import ProxyRequest
from pyasyncproxy.model.dto.ProxyTree import ProxyRootTree
from pyasyncproxy.service.proxy.node.ProxyErrorNode import ProxyErrorNode
from pyasyncproxy.service.proxy.node.ProxyHeaderNode import ProxyHeaderNode
from pyasyncproxy.service.proxy.node.ProxyHttpNode import ProxyHttpNode
from pyasyncproxy.service.proxy.ProxyNode import ProxyNode
from pyasyncproxy.service.proxy.ProxySimpleEngineFactory import ProxySimpleEngineFactory
from pyasyncproxy.service.proxy.ProxySimpleService import ProxySimpleService

logger = logging.getLogger(__name__)

env = ProjectEnv()
with env.proxy_path.open("r") as f:
    proxy_tree = ProxyRootTree.model_validate_json("".join(f.readlines()))
node_map: Mapping[str, ProxyNode] = {
    ProxyHttpNode.__name__: ProxyHttpNode(HttpxClient),
    ProxyHeaderNode.__name__: ProxyHeaderNode(env),
    ProxyErrorNode.__name__: ProxyErrorNode(),
}
proxy_engine_factory = ProxySimpleEngineFactory(node_map)
proxy_engine = ProxySimpleEngineFactory(node_map).create_engine(proxy_tree)
service = ProxySimpleService(proxy_engine)


async def forward_request(req: Request) -> Response:
    """Forward request."""
    url = str(req.url)
    method = req.method
    content = await req.body()
    data = ProxyRequest(request_id=0, url=url, method=method, content=content, headers=req.headers)
    res = await service.forward_request(data)
    return Response(content=res.content, status_code=res.code, headers=res.headers, media_type=res.media_type)


routes = [
    Route("/proxy", endpoint=forward_request, methods=["POST"]),
]
app = Starlette(debug=env.debug, routes=routes)
