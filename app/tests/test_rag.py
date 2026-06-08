from fastapi.testclient import  TestClient
from unittest.mock import patch, AsyncMock
from app.main import app

client = TestClient(app)

@patch("app.routes.rag.ask_document", new_callable=AsyncMock)

def test_ask_doc(mock_ask_document):
    mock_ask_document.return_value = {
        "response": "Pods are containers",
        "sources": [
            {"file":"k8s.pdf", "page": 2}
        ]
    }

    response = client.post("/ask-doc",json={"question":"What is pod?"})

    assert response.status_code == 200

    assert response.json()["response"] == "Pods are containers"