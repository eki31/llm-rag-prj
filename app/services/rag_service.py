from app.rag.retriever import get_retriever
from app.services.openrouter_service import ask_llm
from app.core.logger import logger

async def ask_document(question: str):
    logger.info("Running RAG retrieval")

    retriever = get_retriever()
    results = retriever.invoke(question)
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
            "file":doc.metadata.get("source","unknown"),
            "page":doc.metadata.get("page","unknown")
        }

        sources.append(source)

    return {
        "response" : response,
        "sources" : sources
    }