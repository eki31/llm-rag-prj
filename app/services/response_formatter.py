def format_llm_response(response_json):
    """Extract relevant content for cleaner API response"""
    """Created separate function for easier edit when change API provider """
    try:
        answer = (response_json["choices"][0]["message"]["content"])
        return {"answer": answer}
    except (KeyError,IndexError, TypeError):
        return {"error":"Invalid response format"}