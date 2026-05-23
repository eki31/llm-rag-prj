from langchain_chroma import Chroma

from app.rag.embeddings import get_embedding_model

VECTOR_DB_DIR = "app/vector_db"

retriever_instance = None

def get_retriever():

    global retriever_instance
    if retriever_instance:
        return retriever_instance

    embeddings = get_embedding_model()

    vector_store = Chroma(persist_directory=VECTOR_DB_DIR, embedding_function=embeddings)

    retriever_instance = vector_store.as_retriever(search_kwargs= {"k":5})

    return retriever_instance