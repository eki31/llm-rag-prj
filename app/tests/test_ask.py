from fastapi.testclient import (
    TestClient
)

from unittest.mock import patch, AsyncMock

from app.main import app

client = TestClient(app)


@patch(
"app.routes.ai.ask_llm",
new_callable=AsyncMock
)

def test_ask_endpoint(
    mock_ask_llm
):

    mock_ask_llm.return_value = {
        "answer":
        "Docker explanation"
    }

    response = client.post(
        "/ask",
        json={
            "question":
            "Explain Docker"
        }
    )

    assert (
        response.status_code
        == 200
    )

    assert (
        response.json()
        ["answer"]
        ==
        "Docker explanation"
    )