def test_health_ok(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json().get("status") in ("ok", "OK", "healthy")  

def test_root_or_docs_exists(client):
    r1 = client.get("/")
    r2 = client.get("/docs")
    assert (r1.status_code < 500) or (r2.status_code == 200)

def test_openapi_available(client):
    r = client.get("/openapi.json")
    assert r.status_code == 200
    assert r.json().get("openapi") is not None

def test_404_returns_json(client):
    r = client.get("/this-route-should-not-exist")
    assert r.status_code == 404
    assert "detail" in r.json()

def test_cors_preflight_basic(client):
    r = client.options("/health")
    assert r.status_code in (200, 204, 405)
