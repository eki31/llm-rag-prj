import json
import socket
import threading
from unittest.mock import patch, AsyncMock, MagicMock

import pytest
import redis
from fastapi.testclient import TestClient
from langchain_core.documents import Document

from app.core import cache
from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_cache_backoff():
    cache._unavailable_until = 0.0
    yield
    cache._unavailable_until = 0.0


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

    with patch("app.core.cache.redis_client", FakeRedis()):
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
    fake_redis = FakeRedis()

    with patch("app.core.cache.redis_client", fake_redis):
        response = client.post("/ask-doc", json={"question": "What is pod?"})

    assert response.json()["response"] == {"error": "API request failed"}
    assert fake_redis.store == {}


@patch("app.services.rag_service.get_retriever", side_effect=fake_retriever)
@patch("app.services.rag_service.ask_llm", new_callable=AsyncMock)
def test_old_format_cache_entry_is_treated_as_miss(mock_ask_llm, mock_get_retriever):
    mock_ask_llm.return_value = {"answer": "Pods are containers"}
    fake_redis = FakeRedis()
    fake_redis.store["question: What is pod?"] = json.dumps({"answer": "stale"})

    with patch("app.core.cache.redis_client", fake_redis):
        response = client.post("/ask-doc", json={"question": "What is pod?"})

    assert response.json()["response"] == {"answer": "Pods are containers"}
    assert "cached" not in response.json()
    assert mock_ask_llm.await_count == 1


class DownRedis:
    def __init__(self):
        self.calls = 0

    def get(self, key):
        self.calls += 1
        raise redis.ConnectionError("Error -2 connecting to redis:6379. Name or service not known.")

    def setex(self, key, ttl, value):
        self.calls += 1
        raise redis.ConnectionError("Error -2 connecting to redis:6379. Name or service not known.")


@patch("app.services.rag_service.get_retriever", side_effect=fake_retriever)
@patch("app.services.rag_service.ask_llm", new_callable=AsyncMock)
def test_answers_when_redis_is_down(mock_ask_llm, mock_get_retriever):
    mock_ask_llm.return_value = {"answer": "Pods are containers"}

    with patch("app.core.cache.redis_client", DownRedis()):
        response = client.post("/ask-doc", json={"question": "What is pod?"})

    assert response.status_code == 200
    assert "error" not in response.json()
    assert response.json()["response"] == {"answer": "Pods are containers"}
    assert response.json()["sources"] == [{"file": "k8s.pdf", "page": 2}]


@patch("app.services.rag_service.get_retriever", side_effect=fake_retriever)
@patch("app.services.rag_service.ask_llm", new_callable=AsyncMock)
def test_skips_redis_for_a_while_after_a_failure(mock_ask_llm, mock_get_retriever):
    mock_ask_llm.return_value = {"answer": "Pods are containers"}
    down = DownRedis()

    with patch("app.core.cache.redis_client", down):
        client.post("/ask-doc", json={"question": "What is pod?"})
        client.post("/ask-doc", json={"question": "What is a node?"})

    # Only the first lookup reaches Redis; the rest are skipped during the backoff
    assert down.calls == 1


def test_unreachable_redis_is_tried_only_once():
    # A server that accepts each connection and closes it at once, like a Redis that keeps dropping us
    server = socket.create_server(("127.0.0.1", 0))
    attempts = 0
    stop = threading.Event()

    def drop_connections():
        nonlocal attempts
        server.settimeout(0.1)
        while not stop.is_set():
            try:
                conn, _ = server.accept()
            except TimeoutError:
                continue
            attempts += 1
            conn.close()

    thread = threading.Thread(target=drop_connections)
    thread.start()
    pool_kwargs = cache.redis_client.connection_pool.connection_kwargs
    try:
        with patch.dict(pool_kwargs, {"host": "127.0.0.1", "port": server.getsockname()[1]}):
            cache.redis_client.connection_pool.reset()
            assert cache.cache_get("question: What is pod?") is None
    finally:
        cache.redis_client.connection_pool.reset()
        stop.set()
        thread.join()
        server.close()

    # Retrying would block the event loop for seconds while Redis is down
    assert attempts == 1
