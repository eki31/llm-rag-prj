import json
from unittest.mock import patch, AsyncMock, MagicMock

from fastapi.testclient import TestClient
from langchain_core.documents import Document

from app.main import app

client = TestClient(app)


class FakeRedis:
    def __init__(self):
        self.store = {}

    def get(self, key):
        return self.store.get(key)

    def setex(self, key, ttl, value):
        self.store[key] = value


def fake_retriever():
    retriever = MagicMock()
    retriever.invoke.return_value = [
        Document(page_content="Pods are containers", metadata={"source": "k8s.pdf", "page": 2})
    ]
    return retriever


@patch("app.services.rag_service.get_retriever", side_effect=fake_retriever)
@patch("app.services.rag_service.ask_llm", new_callable=AsyncMock)
def test_cache_hit_returns_same_shape_as_fresh_answer(mock_ask_llm, mock_get_retriever):
    mock_ask_llm.return_value = {"answer": "Pods are containers"}

    with patch("app.services.rag_service.redis_client", FakeRedis()):
        first = client.post("/ask-doc", json={"question": "What is pod?"})
        second = client.post("/ask-doc", json={"question": "What is pod?"})

    assert first.status_code == 200
    assert second.status_code == 200
    assert second.json() == {**first.json(), "cached": True}
    assert second.json()["response"] == {"answer": "Pods are containers"}
    assert second.json()["sources"] == [{"file": "k8s.pdf", "page": 2}]
    assert mock_ask_llm.await_count == 1


@patch("app.services.rag_service.get_retriever", side_effect=fake_retriever)
@patch("app.services.rag_service.ask_llm", new_callable=AsyncMock)
def test_failed_llm_call_is_not_cached(mock_ask_llm, mock_get_retriever):
    mock_ask_llm.return_value = {"error": "API request failed"}
    redis = FakeRedis()

    with patch("app.services.rag_service.redis_client", redis):
        response = client.post("/ask-doc", json={"question": "What is pod?"})

    assert response.json()["response"] == {"error": "API request failed"}
    assert redis.store == {}


@patch("app.services.rag_service.get_retriever", side_effect=fake_retriever)
@patch("app.services.rag_service.ask_llm", new_callable=AsyncMock)
def test_old_format_cache_entry_is_treated_as_miss(mock_ask_llm, mock_get_retriever):
    mock_ask_llm.return_value = {"answer": "Pods are containers"}
    redis = FakeRedis()
    redis.store["question: What is pod?"] = json.dumps({"answer": "stale"})

    with patch("app.services.rag_service.redis_client", redis):
        response = client.post("/ask-doc", json={"question": "What is pod?"})

    assert response.json()["response"] == {"answer": "Pods are containers"}
    assert "cached" not in response.json()
    assert mock_ask_llm.await_count == 1
