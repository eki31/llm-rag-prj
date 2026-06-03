from app.rag.retriever import get_retriever
from app.services.openrouter_service import ask_llm
from app.core.logger import logger

async def ask_document(question: str):
    try:
        logger.info("Running RAG retrieval")
        
        if not question or not question.strip():
            logger.warning("Empty question received")
            return {
                "error": "Question cannot be empty",
                "response": None,
                "sources": []
            }

        retriever = get_retriever()
        results = retriever.invoke(question)
        
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

        prompt = f"""
You are a helpful assistant.
Answer ONLY using the provided context.
    
If answer is not found, say:
"I could not find the answer in the documents."
    
Context:
{context}
    
Question:
{question}    
"""
        response = await ask_llm(prompt)

        sources = []
        for doc in results:
            source = {
                "file": doc.metadata.get("source", "unknown"),
                "page": doc.metadata.get("page", "unknown")
            }
            sources.append(source)

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