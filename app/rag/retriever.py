from langchain_community.vectorstores import Chroma

from app.rag.embeddings import get_embedding_model

VECTOR_DB_DIR = "app/vector_db"

def get_retriever():
    embeddings = get_embedding_model()

    vector_store = Chroma(persist_directory=VECTOR_DB_DIR, embedding_function=embeddings)

    retriever = vector_store.as_retriever(search_kwargs= {"k":3})

    return retriever