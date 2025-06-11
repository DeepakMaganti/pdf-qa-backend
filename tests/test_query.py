import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.mark.skipif(not os.path.exists("data/chroma/index"), reason="Chroma DB missing")
def test_query_endpoint():
    response = client.post(
        "/api/query",
        json={
            "pdf_id": "test",  # or "test.pdf" — use the real ID/filename from Chroma
            "question": "What is this PDF about?"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert isinstance(data["answer"], str)
