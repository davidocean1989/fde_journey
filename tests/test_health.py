from fastapi.testclient import TestClient
import app.api.health as health_mod

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


def test_readyz_reports_not_ready() -> None:
    with TestClient(app) as client:
        resp = client.get("/readyz")
    body = resp.json()
    assert resp.status_code == 200
    assert body["status"] == "ready"
    assert body["checks"]["config"] is True


def test_readyz_returns_503_when_check_fails(monkeypatch) -> None:
    def fake_collect_checks() -> dict[str, bool]:
        return {"config": True, "llm": False}

    monkeypatch.setattr(health_mod, "_collect_checks", fake_collect_checks)

    with TestClient(app) as client:
        resp = client.get("/readyz")

    assert resp.status_code == 503
    body = resp.json()
    assert body["status"] == "not_ready"
    assert body["checks"]["llm"] is False
