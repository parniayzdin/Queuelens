from fastapi.testclient import TestClient
import main  

client = TestClient(main.app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"
