from app.api.v1 import health


def test_health_ok(client, monkeypatch):
    monkeypatch.setattr(health, "check_database", lambda: True)
    r = client.get("/api/v1/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok" and body["database"] == "up"


def test_health_detects_database_failure(client, monkeypatch):
    monkeypatch.setattr(health, "check_database", lambda: False)
    r = client.get("/api/v1/health")
    assert r.status_code == 503
    assert r.json()["database"] == "down"


def test_cors_blocks_unapproved_origin(client):
    r = client.get("/api/v1/health", headers={"Origin": "https://evil.example"})
    assert "access-control-allow-origin" not in r.headers
