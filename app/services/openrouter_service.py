import requests

from app.core.logger import logger

from app.core.config import (
    OPENROUTER_API_KEY,
    OPENROUTER_MODEL
)

URL = "https://openrouter.ai/api/v1/chat/completions"

def ask_llm(question: str):

    logger.info("Sending request to OpenRouter")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {
                "role": "user",
                "content": question
            }
        ]
    }

    response = requests.post(
        URL,
        headers=headers,
        json=payload
    )

    logger.info(f"Open router status code: {response.status_code}")
    return response.json()


def summarize_text(text: str):
    prompt = f"""
    Summarize the following text in simple bullet points:
    
    {text}
    """

    return ask_llm(prompt)
