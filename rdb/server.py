import json
from dataclasses import dataclass, field
from http import HTTPMethod, HTTPStatus
from http.server import BaseHTTPRequestHandler
from socketserver import TCPServer
from typing import Callable, Optional
from urllib.parse import parse_qsl, urlparse

HOST = "127.0.0.1"
PORT = 4000


class RequestParams(dict):
    """
    Simple wrapper for request query params.
    This doesn't support multiple values for a key - the last value is kept.

    For example: /path?a=1&a=2&b=3
    The params stored will be: a=2 and b=3
    """

    def __init__(self, query: str):
        super().__init__(parse_qsl(query))


@dataclass
class Request:
    method: HTTPMethod
    path: str
    params: RequestParams


@dataclass
class Response:
    body: bytes = b""
    status: HTTPStatus = HTTPStatus.OK
    headers: dict[str, str] = field(default_factory=dict)


class JsonResponse(Response):
    def __init__(
        self,
        body: dict,
        status: Optional[HTTPStatus] = None,
        headers: Optional[dict[str, str]] = None,
    ):
        kwargs = {"body": json.dumps(body).encode()}
        if status is not None:
            kwargs["status"] = status
        if headers is None:
            headers = {}
        headers["Content-Type"] = "application/json"
        headers["Content-Length"] = len(kwargs["body"])
        kwargs["headers"] = headers
        super().__init__(**kwargs)


RequestHandler = Callable[[Request], Response]

routes: dict[str, RequestHandler] = {}


def register_route(path: str):
    """Decorator to register handler for a route"""

    def decorator(handler: RequestHandler) -> RequestHandler:
        routes[path] = handler
        return handler

    return decorator


class Handler(BaseHTTPRequestHandler):
    def respond(self, response: Response):
        self.send_response(response.status)
        for header, value in response.headers.items():
            self.send_header(header, value)
        self.end_headers()
        self.wfile.write(response.body)

    def do_request(self, method):
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        handler = routes.get(path)
        if handler is None:
            return self.respond(Response(status=HTTPStatus.NOT_FOUND))
        request = Request(
            method=method,
            path=path,
            params=RequestParams(parsed_url.query),
        )
        response = handler(request)
        self.respond(response)

    def do_GET(self):
        self.do_request(HTTPMethod.GET)


def start_server():
    with TCPServer((HOST, PORT), Handler) as server:
        print(f"listening on {HOST}:{PORT}")
        server.serve_forever()
