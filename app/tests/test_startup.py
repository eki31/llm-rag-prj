from unittest.mock import patch, MagicMock

from fastapi.testclient import TestClient

from app.main import app


@patch("app.main.get_retriever")
def test_retriever_is_warmed_up_at_startup(mock_get_retriever):
    retriever = MagicMock()
    mock_get_retriever.return_value = retriever

    # Using TestClient as a context manager runs the app's startup (lifespan)
    with TestClient(app) as client:
        assert client.get("/health").status_code == 200

    mock_get_retriever.assert_called_once()
    retriever.invoke.assert_called_once()


@patch("app.main.get_retriever", side_effect=RuntimeError("vector store missing"))
def test_startup_survives_warm_up_failure(mock_get_retriever):
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
