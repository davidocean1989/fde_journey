from fastapi.testclient import TestClient

from app.main import app


def test_healthz_ok() -> None:
    with TestClient(app) as client:
        resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_readyz_reports_checks() -> None:
    with TestClient(app) as client:
        resp = client.get("/readyz")
    body = resp.json()
    assert resp.status_code == 200
    assert body["status"] == "ready"
    assert body["checks"]["config"] is True
