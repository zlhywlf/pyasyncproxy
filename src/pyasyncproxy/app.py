"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import logging

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Route

from pyasyncproxy.client.CacheLocalClient import CacheLocalClient
from pyasyncproxy.client.DynamicIpLocalPool import DynamicIpLocalPool
from pyasyncproxy.common.Snowflake import Snowflake
from pyasyncproxy.model.dto.ProjectEnv import ProjectEnv
from pyasyncproxy.model.dto.ProxyContext import ProxyContext
from pyasyncproxy.model.dto.ProxyRequest import ProxyRequest
from pyasyncproxy.model.dto.ProxyTree import ProxyRootTree
from pyasyncproxy.service.proxy.ProxySimpleEngineFactory import ProxySimpleEngineFactory
from pyasyncproxy.service.proxy.ProxySimpleNodeFactory import ProxySimpleNodeFactory
from pyasyncproxy.service.proxy.ProxySimpleService import ProxySimpleService

logger = logging.getLogger(__name__)

env = ProjectEnv()
snowflake = Snowflake(env.worker_id, env.data_center_id)
with env.proxy_path.open("r") as f:
    proxy_tree = ProxyRootTree.model_validate_json("".join(f.readlines()))
nodes_map = ProxySimpleNodeFactory().collect_nodes()
proxy_engine_factory = ProxySimpleEngineFactory(nodes_map)
cache_client = CacheLocalClient()
dynamic_ip_pool = DynamicIpLocalPool()
proxy_engine = proxy_engine_factory.create_engine(proxy_tree)
service = ProxySimpleService(proxy_engine)


async def forward_request(req: Request) -> Response:
    """Forward request."""
    url = req.url.__str__()
    method = req.method
    content = await req.body()
    request_id = snowflake.next_id()
    data = ProxyRequest(url=url, method=method, content=content, headers=req.headers)
    ctx = ProxyContext(
        request_id=request_id, data=data, env=env, cache_client=cache_client, dynamic_ip_pool=dynamic_ip_pool
    )
    res = await service.forward_request(ctx)
    return Response(content=res.content, status_code=res.code, headers=res.headers, media_type=res.media_type)


routes = [
    Route("/proxy", endpoint=forward_request, methods=["POST"]),
]
app = Starlette(debug=env.debug, routes=routes)
