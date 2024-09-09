"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Route

from pyasyncproxy.bake.proxy import env, service
from pyasyncproxy.model.dto.ProxyRequest import ProxyRequest


async def forward_request(req: Request) -> Response:
    """Forward request."""
    request = ProxyRequest(url=req.url.__str__(), method=req.method, content=await req.body(), headers=req.headers)
    res = await service.forward_request(request)
    return Response(content=res.content, status_code=res.code, headers=res.headers, media_type=res.media_type)


routes = [
    Route("/proxy", endpoint=forward_request, methods=["POST"]),
]
app = Starlette(debug=env.debug, routes=routes)
