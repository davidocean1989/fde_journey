"""统一错误形状的测试：这条测试的价值在于锁住契约。

以后谁改了错误结构，CI 会立刻红——而不是等客户在群里发截图。
"""

from fastapi.testclient import TestClient

from app.core.errors import BadRequestError
from app.main import app


def test_app_error_shape() -> None:
    @app.get("/__test/bad")
    async def _bad() -> None:
        raise BadRequestError("参数不对", code="invalid_param")

    with TestClient(app, raise_server_exceptions=False) as client:
        resp = client.get("/__test/bad")

    assert resp.status_code == 400
    body = resp.json()
    assert set(body["error"]) == {"code", "message", "request_id"}
    assert body["error"]["code"] == "invalid_param"


def test_unhandled_error_returns_500_and_hides_detail() -> None:
    @app.get("/__test/boom")
    async def _boom() -> None:
        raise RuntimeError("boom")  # 根 AppError 无血缘，必走兜底

    with TestClient(app, raise_server_exceptions=False) as client:
        resp = client.get("/__test/boom")

    assert resp.status_code == 500
    body = resp.json()
    assert set(body["error"]) == {"code", "message", "request_id"}
    assert body["error"]["code"] == "internal_error"
    assert "boom" not in body["error"]["message"]


def test_custom_status_code_overrides_default() -> None:
    @app.get("/__test/teapot")
    async def _teapot() -> None:
        raise BadRequestError("y", status_code=418)

    with TestClient(app, raise_server_exceptions=False) as client:
        resp = client.get("/__test/teapot")

    assert resp.status_code == 418
    body = resp.json()
    assert set(body["error"]) == {"code", "message", "request_id"}
    assert body["error"]["code"] == "bad_request"
    assert body["error"]["message"] == "y"
