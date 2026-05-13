#to run : python -m app.tests.test_loader
from app.rag.chunker import chunk_documents
from app.rag.document_loader import load_documents
from app.rag.embeddings import get_embedding_model
from app.rag.vector_store import create_vector_store
from app.rag.retriever import get_retriever

documents = load_documents()
#print(documents[1].page_content)

chunks = chunk_documents(documents)
print(chunks[1].page_content)

embeddings = get_embedding_model()

vector_store = create_vector_store(chunks,embeddings)

print("Vector DB created")

retriever = get_retriever()

results = retriever.invoke("Explain how Spanning Tree work")

for result in results:
    print(result.page_content)
    print("=" * 50)