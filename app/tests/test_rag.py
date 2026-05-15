from fastapi.testclient import  TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)

@patch("app.services.rag_service.ask_document")

def test_ask_doc(mock_ask_document):
    mock_ask_document.return_value = {
        "response": {"answer":"Pods are containers"},
        "sources": [
            {"file":"k8s.pdf", "page": 2}
        ]
    }

    response = client.post("/ask-doc",json={"question":"What is pod?"})

    assert response.status_code == 200

    assert response.json()["response"]["answer"] == "Pods are containers"