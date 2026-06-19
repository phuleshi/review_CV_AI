"""Shared pytest fixtures."""
import asyncio
import json
from typing import Any
from urllib.parse import urlsplit

import httpx
import pytest

from app.main import app


class ASGITestClient:
    def __init__(self, asgi_app) -> None:
        self._app = asgi_app

    def request(self, method: str, url: str, **kwargs: Any) -> httpx.Response:
        body, headers = self._build_body_and_headers(kwargs)

        async def _request() -> httpx.Response:
            parsed = urlsplit(url)
            scope = {
                "type": "http",
                "asgi": {"version": "3.0"},
                "http_version": "1.1",
                "method": method,
                "scheme": "http",
                "path": parsed.path,
                "raw_path": parsed.path.encode(),
                "query_string": parsed.query.encode(),
                "headers": [(k.lower().encode(), v.encode()) for k, v in headers.items()],
                "client": ("testclient", 50000),
                "server": ("testserver", 80),
                "root_path": "",
            }
            request_messages = [{"type": "http.request", "body": body, "more_body": False}]
            response_status = 500
            response_headers: list[tuple[bytes, bytes]] = []
            response_body = bytearray()

            async def receive() -> dict[str, Any]:
                if request_messages:
                    return request_messages.pop(0)
                return {"type": "http.disconnect"}

            async def send(message: dict[str, Any]) -> None:
                nonlocal response_status, response_headers
                if message["type"] == "http.response.start":
                    response_status = message["status"]
                    response_headers = message.get("headers", [])
                elif message["type"] == "http.response.body":
                    response_body.extend(message.get("body", b""))

            await self._app(scope, receive, send)
            return httpx.Response(
                status_code=response_status,
                headers={k.decode(): v.decode() for k, v in response_headers},
                content=bytes(response_body),
                request=httpx.Request(method, f"http://testserver{url}"),
            )

        return asyncio.run(_request())

    def get(self, url: str, **kwargs: Any) -> httpx.Response:
        return self.request("GET", url, **kwargs)

    def post(self, url: str, **kwargs: Any) -> httpx.Response:
        return self.request("POST", url, **kwargs)

    @staticmethod
    def _build_body_and_headers(kwargs: dict[str, Any]) -> tuple[bytes, dict[str, str]]:
        headers = dict(kwargs.pop("headers", {}) or {})
        if "json" in kwargs:
            headers.setdefault("content-type", "application/json")
            return json.dumps(kwargs["json"]).encode(), headers
        if "files" in kwargs:
            boundary = "pytest-boundary"
            headers.setdefault("content-type", f"multipart/form-data; boundary={boundary}")
            body = bytearray()
            for field, file_info in kwargs["files"].items():
                filename, content, content_type = file_info
                body.extend(f"--{boundary}\r\n".encode())
                body.extend(
                    (
                        f'Content-Disposition: form-data; name="{field}"; '
                        f'filename="{filename}"\r\n'
                    ).encode()
                )
                body.extend(f"Content-Type: {content_type}\r\n\r\n".encode())
                body.extend(content)
                body.extend(b"\r\n")
            body.extend(f"--{boundary}--\r\n".encode())
            return bytes(body), headers
        return b"", headers


@pytest.fixture
def client() -> ASGITestClient:
    return ASGITestClient(app)
