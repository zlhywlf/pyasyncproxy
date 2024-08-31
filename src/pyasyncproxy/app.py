"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import contextlib
import logging
from collections.abc import AsyncGenerator, Mapping
from typing import Any

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import Response

from pyasyncproxy.env.ProjectEnv import ProjectEnv
from pyasyncproxy.model.dto.ProxyRequest import ProxyRequest
from pyasyncproxy.model.dto.ProxyTree import ProxyRootTree
from pyasyncproxy.service.proxy.ProxyNode import ProxyNode
from pyasyncproxy.service.proxy.ProxySimpleEngineFactory import ProxySimpleEngineFactory
from pyasyncproxy.service.proxy.ProxySimpleService import ProxySimpleService

logger = logging.getLogger(__name__)

env = ProjectEnv()
proxy_tree = ProxyRootTree.model_validate({"name": ""})
node_map: Mapping[str, ProxyNode] = {}
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


@contextlib.asynccontextmanager
async def lifespan(app: Starlette) -> AsyncGenerator[dict[str, Any], Any]:
    """Lifespan."""
    app.add_route("/", forward_request, ["POST", "GET"])
    yield {}
    logger.info("app stopped")


app = Starlette(debug=env.debug, lifespan=lifespan)
