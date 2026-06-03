
# AI Knowledge Assistant API - Phase 1 & Phase 2

A production-style AI backend API built with **FastAPI**, integrated with **OpenRouter LLM APIs**, containerized using **Docker**, and enhanced with asynchronous request handling, structured logging, unit testing, and **Retrieval-Augmented Generation (RAG)** capabilities.

**Phase 1**: Foundation - Core API, LLM integration, async patterns, Docker containerization
**Phase 2**: RAG System - Document ingestion, vector embeddings, semantic search, grounded responses

This project was built as part of my MLOps learning roadmap to strengthen backend engineering, API development, Docker, production engineering fundamentals, and modern AI/ML system design (RAG, embeddings, vector databases).

---

# Features

## Phase 1: Core LLM Features

### Health Check Endpoint
Simple health endpoint for service availability verification.

```http
GET /health
```

Response:

```json
{
  "status": "healthy"
}
```

---

### Ask AI Endpoint
Send a question directly to an LLM through OpenRouter (no document context).

```http
POST /ask
```

Request:

```json
{
  "question": "Explain Kubernetes simply"
}
```

Response:

```json
{
  "answer": "Kubernetes is a platform used to manage containers..."
}
```

---

### Summarize Endpoint
Summarizes input text using prompt engineering logic handled by the backend.

```http
POST /summarize
```

Request:

```json
{
  "text": "Docker is a containerization platform..."
}
```

Response:

```json
{
  "answer": "Docker packages applications into portable containers."
}
```

---

## Phase 2: RAG System Features

### Load Documents Endpoint
Ingest PDF documents from uploads folder into the vector database. This endpoint:
- Loads all PDFs from `app/uploads/`
- Splits documents into chunks (500 characters with 100-char overlap)
- Creates embeddings using `sentence-transformers/all-MiniLM-L6-v2`
- Stores embeddings in persistent ChromaDB
- Returns ingestion statistics

```http
POST /load-docs
```

Response:

```json
{
  "status": "success",
  "message": "Documents ingested successfully",
  "documents_loaded": 42,
  "chunks_created": 847
}
```

---

### Ask Document Endpoint (RAG)
Query documents with grounded responses. This endpoint:
- Retrieves semantically similar document chunks (top 5)
- Sends retrieved context + question to OpenRouter LLM
- Returns answer grounded in document context + source metadata

```http
POST /ask-doc
```

Request:

```json
{
  "question": "What is Spanning Tree Protocol?"
}
```

Response:

```json
{
  "response": {
    "answer": "Spanning Tree Protocol (STP) is a network protocol that prevents loops in Ethernet networks..."
  },
  "sources": [
    {
      "file": "CCNA 200-301 Notes.pdf",
      "page": 42
    }
  ]
}
```

---

# Tech Stack

## Phase 1 - Core

- **Python** - Programming language
- **FastAPI** - Web framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation
- **HTTPX** - Async HTTP client
- **Python-dotenv** - Environment variables
- **Docker** - Containerization
- **Pytest** - Testing framework

## Phase 2 - RAG System

- **LangChain** - LLM application framework
- **ChromaDB** - Vector database (persistent)
- **sentence-transformers** - Embedding model (`all-MiniLM-L6-v2`)
- **PyPDF** - PDF loading
- **Chroma client** - Vector storage and retrieval

## External APIs

- **OpenRouter API** - LLM provider (supports multiple models)

---

# Architecture

## Phase 1: Direct LLM Query

```text
Client
   ↓
FastAPI Routes
   ↓
Validation (Pydantic)
   ↓
Service Layer
   ↓
OpenRouter API
   ↓
Response Formatter
   ↓
JSON Response
```

---

## Phase 2: Retrieval-Augmented Generation (RAG)

### Document Ingestion Pipeline

```text
PDF Files (app/uploads/)
   ↓
Document Loader (PyPDF)
   ↓
Text Chunker (LangChain - 500 char chunks)
   ↓
Embedding Model (sentence-transformers)
   ↓
Vector Store (ChromaDB - persistent)
```

### Query Pipeline

```text
Question
   ↓
Vector Embedding (same model)
   ↓
Semantic Search (ChromaDB retriever - top 5 chunks)
   ↓
Retrieved Context + Question
   ↓
OpenRouter LLM (grounded generation)
   ↓
Answer + Source Metadata
```

---

# Project Structure

```text
ai-knowledge-api/
│
├── app/
│   ├── main.py
│   │
│   ├── routes/
│   │   ├── ai.py              (Phase 1: /ask, /summarize, /health)
│   │   └── rag.py             (Phase 2: /load-docs, /ask-doc)
│   │
│   ├── services/
│   │   ├── openrouter_service.py
│   │   ├── response_formatter.py
│   │   ├── rag_service.py      (Phase 2: RAG pipeline)
│   │   └── ingest_service.py   (Phase 2: document ingestion)
│   │
│   ├── rag/                    (Phase 2: RAG components)
│   │   ├── document_loader.py  (PDF loading)
│   │   ├── chunker.py          (Text splitting)
│   │   ├── embeddings.py       (Embedding model)
│   │   ├── vector_store.py     (ChromaDB storage)
│   │   ├── retriever.py        (Vector retrieval)
│   │   └── vector_db/          (Persistent ChromaDB)
│   │       └── chroma.sqlite3
│   │
│   ├── models/
│   │   └── schemas.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── logger.py
│   │
│   ├── uploads/                (Phase 2: PDF input directory)
│   └── tests/
│       ├── __init__.py
│       ├── test_health.py
│       ├── test_ask.py
│       ├── test_loader.py      (Phase 2: RAG pipeline test)
│       └── test_rag.py         (Phase 2: RAG endpoint test)
│
├── .env
├── requirements.txt
├── Dockerfile
├── memo.md
├── reset_vector_db.sh
└── README.md
```

---

# Key Engineering Concepts Implemented

## 1. Response Formatting
Implemented an abstraction layer to normalize raw LLM responses into a cleaner API response format.

Instead of exposing raw vendor-specific JSON, the API returns structured outputs.

Example:

Before:

```json
{
  "choices": [
    {
      "message": {
        "content": "Docker explanation"
      }
    }
  ]
}
```

After:

```json
{
  "answer": "Docker explanation"
}
```

This improves maintainability and vendor portability.

---

## 2. Asynchronous API Requests
Implemented asynchronous external API requests using **HTTPX AsyncClient**.

Benefits:

- Better concurrency
- Improved scalability
- Non-blocking request handling
- More production-ready architecture

---

## 3. Structured Logging
Implemented logging for:

- incoming requests
- OpenRouter API calls
- response status tracking
- error debugging

Example logs:

```text
INFO - Question received
INFO - Sending request to OpenRouter
INFO - Success: 200
```

---

## 4. Error Handling
Implemented graceful error handling for:

- request timeout
- invalid API responses
- HTTP errors
- unexpected failures

This prevents application crashes and improves reliability.

---

## 5. Unit Testing
Implemented endpoint testing using **Pytest** and mocking.

Tests include:

- health endpoint validation
- ask endpoint validation

Mocking is used to avoid real API calls during tests.

---

# Running Locally

## Clone repository

```bash
git clone <your-repo-url>
cd ai-knowledge-api
```

---

## Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Install dependencies

```bash
pip install -r requirements.txt
```

---

## Configure environment variables

Create `.env`

```env
OPENROUTER_API_KEY=your_api_key
OPENROUTER_MODEL=openai/gpt-4o-mini
```

---

## Run server

```bash
uvicorn app.main:app --reload
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

---

# Run Tests

```bash
pytest
```

---

# Learning Outcomes

## Phase 1 - Backend Fundamentals

Through Phase 1, I practiced:

- Backend API development with FastAPI
- REST API design principles
- Asynchronous programming (async/await)
- Error handling and graceful degradation
- Structured logging for debugging
- Unit testing with Pytest and mocking
- Docker containerization
- Production-style project structure
- External API integration patterns

## Phase 2 - AI/ML Systems

Through Phase 2, I practiced:

- **Retrieval-Augmented Generation (RAG)** - Modern approach to grounded LLM responses
- **Vector Databases** - Persistent storage and semantic search with ChromaDB
- **Embedding Models** - Converting text to semantic vectors
- **Document Processing** - PDF loading, chunking, and preprocessing
- **LangChain Framework** - Building complex LLM application pipelines
- **Semantic Search** - Similarity-based document retrieval
- **Context-Aware Responses** - Augmenting LLM with external knowledge
- **Production RAG System** - End-to-end document QA system

---

# Next Steps & Future Improvements

## Short-term (Production Ready)

- [ ] API authentication and authorization
- [ ] Rate limiting
- [ ] Request tracing / request IDs
- [ ] Input validation and sanitization
- [ ] API documentation improvements

## Medium-term (Enhanced RAG)

- [ ] Multi-document type support (Word, Excel, Markdown, etc.)
- [ ] Hybrid search (keyword + semantic)
- [ ] Metadata filtering for queries
- [ ] LLM-based query expansion
- [ ] Document versioning and updates
- [ ] Batch document ingestion optimization

## Long-term (Production Deployment)

- [ ] CI/CD pipeline with GitHub Actions
- [ ] Kubernetes deployment
- [ ] Monitoring with Prometheus/Grafana
- [ ] Distributed vector database (Qdrant, Milvus)
- [ ] Fine-tuned embedding models
- [ ] Multi-user support with document access control
- [ ] Streaming response support
- [ ] Analytics and usage tracking


# Phase 2: Production-Style RAG System

## What is RAG (Retrieval-Augmented Generation)?

RAG is a modern AI/ML pattern that combines:
1. **Retrieval** - Finding relevant documents/context based on semantic similarity
2. **Augmentation** - Enriching user queries with retrieved context
3. **Generation** - Using LLM to generate answers grounded in that context

**Problem it solves:**
- Raw LLMs hallucinate or use outdated information
- Users need answers grounded in specific documents
- Need to add domain-specific knowledge without fine-tuning

**RAG Solution:**
- Store documents as semantic vectors in a vector database
- When user asks a question, retrieve relevant documents
- Feed retrieved documents + question to LLM
- Get accurate, sourced answers

---

## Implementation Details

### 1. Document Ingestion (`/load-docs` endpoint)

**Flow:**
```
PDF Files → Document Loader → Text Chunking → Embeddings → Vector Store
```

**Components:**
- **document_loader.py** - PyPDF loader reads PDFs from `app/uploads/`
- **chunker.py** - RecursiveCharacterTextSplitter creates overlapping chunks (500 chars, 100 overlap)
- **embeddings.py** - `sentence-transformers/all-MiniLM-L6-v2` converts text → vectors
- **vector_store.py** - ChromaDB stores vectors persistently
- **retriever.py** - Creates retriever for semantic search

**Key Features:**
- Persistent storage in `app/vector_db/chroma.sqlite3`
- Explicit collection naming for reliable persistence
- Error handling and detailed logging
- Returns ingestion statistics (documents loaded, chunks created)

### 2. Query Processing (`/ask-doc` endpoint)

**Flow:**
```
Question → Semantic Search → Retrieve Top-K Chunks → Augment Prompt → LLM → Answer + Sources
```

**Process:**
1. User sends question
2. Question is embedded using the same model
3. ChromaDB retriever finds top 5 most similar document chunks
4. Retrieved context is combined with the question in a prompt
5. OpenRouter LLM generates grounded response
6. Response includes document sources and page numbers

**Key Features:**
- Grounded responses (answers based on actual documents)
- Source attribution (know which documents were used)
- Semantic search (finds relevant content even without exact keyword matches)
- Error handling for empty vector stores or no results

### 3. Vector Database (ChromaDB)

**Why ChromaDB:**
- Lightweight, embeddable vector database
- Persistent storage on disk
- Supports similarity search
- Easy integration with LangChain
- No external database setup needed

**Persistence:**
- Stored in `app/vector_db/chroma.sqlite3`
- Collection-based organization (`documents` collection)
- Survives application restarts

### 4. Embedding Model

**Model:** `sentence-transformers/all-MiniLM-L6-v2`
- Lightweight (33M parameters)
- Fast inference
- Good semantic understanding
- Suitable for general-purpose document retrieval

**Why same model for indexing and querying:**
- Ensures query embeddings match document embeddings
- Critical for accurate semantic search

---

## Usage Workflow

### Step 1: Add Documents
```bash
# Copy PDFs to app/uploads/
cp my_documents.pdf app/uploads/
```

### Step 2: Ingest Documents
```bash
# Call the /load-docs endpoint
curl -X POST http://localhost:8000/load-docs
```

Response:
```json
{
  "status": "success",
  "message": "Documents ingested successfully",
  "documents_loaded": 42,
  "chunks_created": 847
}
```

### Step 3: Query Documents
```bash
# Call the /ask-doc endpoint
curl -X POST http://localhost:8000/ask-doc \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Spanning Tree Protocol?"}'
```

Response:
```json
{
  "response": {
    "answer": "Spanning Tree Protocol (STP) prevents loops in Ethernet networks by creating a loop-free logical tree topology..."
  },
  "sources": [
    {"file": "CCNA 200-301 Notes.pdf", "page": 42}
  ]
}
```

---

## Troubleshooting

### Empty Vector Store

If you get "Vector store is empty - no documents loaded":
1. Ensure PDFs are in `app/uploads/`
2. Run `/load-docs` endpoint first
3. Check logs for PDF loading errors

### Vector DB Persistence Issues

If documents disappear after restart:
1. Verify `app/vector_db/chroma.sqlite3` exists
2. Check file permissions
3. Ensure same embedding model is used (don't change models between runs)

### Clear Vector Store

```bash
# Delete vector database
./app/reset_vector_db.sh

# Or manually
rm -rf app/vector_db/*
```

---

## Key Improvements Over Phase 1

| Aspect | Phase 1 | Phase 2 |
|--------|---------|---------|
| Knowledge Source | Internet (LLM training data) | User's documents |
| Hallucination Risk | High | Low (grounded in docs) |
| Source Attribution | None | Included |
| Domain Specificity | Generic | Custom (user's documents) |
| Freshness | Outdated | Current (user controls) |
| Use Cases | General questions | Document QA, KB search |

---

## Future Enhancements

- Multi-document type support (Word, Excel, HTML, etc.)
- Hybrid search (keyword + semantic)
- Metadata filtering
- LLM-based query expansion
- Streaming responses
- Fine-grained source tracking (exact sentence references)
- Document versioning
- Performance optimization (batch ingestion)
- API authentication and rate limiting