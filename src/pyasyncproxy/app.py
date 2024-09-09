"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Route

from pyasyncproxy.bake.proxy import env, service
from pyasyncproxy.model.dto.ProxyRequest import ProxyRequest
from pyasyncproxy.model.po.ProxyUrl import ProxyUrl


async def forward_request(req: Request) -> Response:
    """Forward request."""
    request = ProxyRequest(url=req.url.__str__(), method=req.method, content=await req.body(), headers=req.headers)
    res = await service.forward_request(request)
    return Response(content=res.content, status_code=res.code, headers=res.headers, media_type=res.media_type)


async def get_proxy_pool(req: Request) -> Response:  # noqa: ARG001
    """Get proxy pool."""
    pool = await service.get_proxy_pool()
    return JSONResponse(content=[_.model_dump() for _ in pool])


async def add_proxy_url(req: Request) -> Response:
    """Add proxy url."""
    await service.add_proxy_url(ProxyUrl.model_validate_json(await req.body()))
    return Response(content="ok")


routes = [
    Route("/proxy", endpoint=forward_request, methods=["POST"]),
    Route("/proxy/info", endpoint=get_proxy_pool, methods=["POST"]),
    Route("/proxy/add", endpoint=add_proxy_url, methods=["POST"]),
]
app = Starlette(debug=env.debug, routes=routes)
