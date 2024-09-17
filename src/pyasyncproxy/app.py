"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import base64
import binascii
from typing import override

from starlette.applications import Starlette
from starlette.authentication import AuthCredentials, AuthenticationBackend, AuthenticationError, BaseUser, SimpleUser
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.requests import HTTPConnection, Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Route

from pyasyncproxy.bake.proxy import env, service
from pyasyncproxy.model.dto.ProxyRequest import ProxyRequest
from pyasyncproxy.model.po.ProxyUrl import ProxyUrl


async def forward_request(req: Request) -> Response:
    """Forward request."""
    proxy_info: BaseUser = req.user
    proxy_url = ProxyUrl.model_validate_json(proxy_info.display_name) if proxy_info.display_name else None
    request = ProxyRequest(
        url="", method=req.method, content=await req.body(), headers=req.headers, proxy_url=proxy_url
    )
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


class ProxyAuthBackend(AuthenticationBackend):
    """proxy auth backend."""

    @override
    async def authenticate(self, conn: HTTPConnection) -> tuple[AuthCredentials, BaseUser] | None:
        try:
            auth = conn.headers["Proxy-Authorization"]
            scheme, credentials = auth.split()
            if scheme.lower() != "basic":
                return None
            decoded = base64.b64decode(credentials).decode()
        except (KeyError, ValueError, UnicodeDecodeError, binascii.Error) as e:
            msg = "Invalid basic auth credentials"
            raise AuthenticationError(msg) from e
        _, _, proxy_url = decoded.partition(":")
        k = env.forward_url_key.encode()
        if not any(_[0] == k for _ in conn.scope["headers"]):
            conn.scope["headers"].append((k, conn.scope["raw_path"]))
        conn.scope["raw_path"] = b"/proxy"
        conn.scope["path"] = "/proxy"
        return AuthCredentials(["proxy"]), SimpleUser(proxy_url)


routes = [
    Route("/proxy", endpoint=forward_request, methods=["GET", "POST"]),
    Route("/proxy/info", endpoint=get_proxy_pool, methods=["POST"]),
    Route("/proxy/add", endpoint=add_proxy_url, methods=["POST"]),
]
middleware = [
    Middleware(AuthenticationMiddleware, backend=ProxyAuthBackend()),
]
app = Starlette(debug=env.debug, routes=routes, middleware=middleware)
