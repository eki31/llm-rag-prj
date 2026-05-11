import requests

from app.core.logger import logger

from app.core.config import (
    OPENROUTER_API_KEY,
    OPENROUTER_MODEL
)

URL = "https://openrouter.ai/api/v1/chat/completions"

def ask_llm(question: str):
    try:
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
            json=payload,
            timeout=30
        )

        response.raise_for_status()

        logger.info(f"Open router status code: {response.status_code}")
        return response.json()

    except requests.Timeout:
        logger.error("OpenRouter timeout")
        return { "error":"Request timeout"}
    except requests.HTTPError as e:
        logger.error(f"HTTP error : {str(e)}")
        return { "error":"API request failed"}
    except Exception as e:
        logger.error(f"Unexpected error : {str(e)}")
        return { "error":"Internal server error"}


def summarize_text(text: str):
    prompt = f"""
    Summarize the following text in simple bullet points:
    
    {text}
    """

    return ask_llm(prompt)
