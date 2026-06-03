# AI Knowledge Assistant API

A production-ready AI backend with **LLM integration** (Phase 1) and **Retrieval-Augmented Generation (RAG)** capabilities (Phase 2).

**Phase 1**: Core API, OpenRouter LLM integration, async patterns
**Phase 2**: Document ingestion, vector embeddings, grounded responses

---

## Features

### Phase 1: Direct LLM Query
- `GET /health` - Health check
- `POST /ask` - Query LLM directly
- `POST /summarize` - Summarize text

### Phase 2: Document QA (RAG)
- `POST /load-docs` - Ingest PDFs into vector database
- `POST /ask-doc` - Query documents with grounded responses + sources

---

## Tech Stack

| Phase 1 | Phase 2 |
|---------|---------|
| FastAPI, Uvicorn | LangChain, ChromaDB |
| HTTPX (async) | sentence-transformers |
| Pydantic | PyPDF |
| Docker, Pytest | OpenRouter API |

---

## Architecture

```
Phase 1: Direct LLM Query
Client → FastAPI Routes → Service Layer → OpenRouter → Response

Phase 2: RAG Pipeline
Documents → Loader → Chunker → Embeddings → ChromaDB (persistent)
Question → Retriever → LLM → Answer + Sources
```

---

## Quick Start

### Setup
```bash
# Clone and install
git clone <repo>
cd ai-knowledge-api
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Configure
echo "OPENROUTER_API_KEY=your_key" > .env
echo "OPENROUTER_MODEL=openai/gpt-4o-mini" >> .env
```

### Run
```bash
# From app directory
cd app
uvicorn main:app --reload

# Access Swagger UI
http://localhost:8000/docs
```

### Phase 2 Usage
```bash
# 1. Add PDFs to app/uploads/

# 2. Ingest documents
curl -X POST http://localhost:8000/load-docs

# 3. Query documents
curl -X POST http://localhost:8000/ask-doc \
  -H "Content-Type: application/json" \
  -d '{"question": "Your question here?"}'
```

---

## Key Features Implemented

✅ **Asynchronous API** - HTTPX AsyncClient for non-blocking requests
✅ **Error Handling** - Graceful degradation, detailed logging
✅ **RAG System** - Document ingestion, semantic search, grounded responses
✅ **Vector Database** - Persistent ChromaDB storage
✅ **Source Attribution** - Know which documents were used
✅ **Production Ready** - Structured logging, unit testing, Docker support

---

## Learning Outcomes

**Phase 1**: FastAPI, async patterns, API design, Docker, testing
**Phase 2**: RAG systems, embeddings, vector databases, semantic search, LLM pipelines

---

## Project Structure

```
ai-knowledge-api/
├── app/
│   ├── routes/          (API endpoints)
│   ├── services/        (business logic)
│   ├── rag/            (RAG components)
│   ├── models/         (Pydantic schemas)
│   └── core/           (config, logging)
├── requirements.txt
├── Dockerfile
└── README.md           (detailed docs)
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| PDF not loading | Ensure PDFs are in `app/uploads/`, call `/load-docs` first |
| Empty vector store | Run `/load-docs` endpoint to ingest documents |
| No documents found | Verify `app/vector_db/chroma.sqlite3` exists |

---

## Future Roadmap

- [ ] Multi-document type support (Word, Excel, etc.)
- [ ] Hybrid search (keyword + semantic)
- [ ] API authentication
- [ ] Kubernetes deployment
- [ ] Monitoring (Prometheus/Grafana)

---

For detailed documentation, see [README.md](README_comprehensive.md)
