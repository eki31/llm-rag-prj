import json
from app.rag.retriever import get_retriever
from app.services.openrouter_service import ask_llm
from app.core.logger import logger
from app.core.memory import conversation_memory
from app.core.cache import redis_client
from app.core.metrics import RAG_REQUEST_COUNT, CACHE_HITS, CACHE_MISSES, OPENROUTER_CALLS


async def ask_document(question: str):
    try:
        RAG_REQUEST_COUNT.inc()
        logger.info("Running RAG retrieval")
        
        if not question or not question.strip():
            logger.warning("Empty question received")
            return {
                "error": "Question cannot be empty",
                "response": None,
                "sources": []
            }

        cache_key = f"question: {question}"
        cached_answer = redis_client.get(cache_key)
        if cached_answer:
            CACHE_HITS.inc()
            return {"response": {cached_answer}, "cached": True}
        CACHE_MISSES.inc()

        retriever = get_retriever()
        results = retriever.invoke(question)
        #Metadata deduplication (remove duplicate pages/files)
        unique_results = []
        seen_sources = set()

        for doc in results:
            source_key = (doc.metadata.get("source"), doc.metadata.get("page"))

            if source_key not in seen_sources:
                seen_sources.add(source_key)
                unique_results.append(doc)

        results = unique_results
        
        if not results:
            logger.warning("No documents retrieved from vector store")
            return {
                "warning": "No relevant documents found",
                "response": "I could not find relevant documents to answer your question.",
                "sources": []
            }
        
        context = "\n\n".join(
            [doc.page_content for doc in results]
        )

        history = "\n".join(conversation_memory[-5:])

        prompt = f"""
You are a helpful assistant.
Answer ONLY using the provided context.
    
If answer is not found, say:
"I could not find the answer in the documents."

Previous conversation:
{history}
    
Context:
{context}
    
Question:
{question}    
"""

        OPENROUTER_CALLS.inc()
        response = await ask_llm(prompt)

        conversation_memory.append(f"User: {question}")
        conversation_memory.append(f"Assistant: {response}")

        sources = []
        for doc in results:
            source = {
                "file": doc.metadata.get("source", "unknown"),
                "page": doc.metadata.get("page", "unknown")
            }
            sources.append(source)

        redis_client.setex(cache_key, 3600, json.dumps(response))

        return {
            "response": response,
            "sources": sources
        }
    except Exception as e:
        logger.error(f"Error in ask_document: {str(e)}", exc_info=True)
        return {
            "error": f"Failed to process question: {str(e)}",
            "response": None,
            "sources": []
        }