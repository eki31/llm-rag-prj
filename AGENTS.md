# AGENTS.md

Project instructions for coding agents working on ai-knowledge-api.
CLAUDE.md is a symlink to this file, so edit AGENTS.md only.

## What this is

A FastAPI backend that answers questions with an LLM through OpenRouter, plus a RAG pipeline over uploaded PDFs.
It also has a Redis answer cache and Prometheus metrics, with a Grafana dashboard.

## Layout

- `app/main.py` - FastAPI app, router registration, and the metrics middleware.
- `app/routes/` - HTTP endpoints (`ai.py`, `rag.py`, `upload.py`, `metrics.py`). Keep them thin.
- `app/services/` - Business logic: OpenRouter calls, RAG answering, ingestion, response formatting.
- `app/rag/` - RAG building blocks: loader, chunker, embeddings, vector store, retriever.
- `app/core/` - Config, logger, Redis cache, conversation memory, Prometheus metrics.
- `app/models/schemas.py` - Pydantic request and response models.
- `app/tests/` - Pytest tests.
- `monitoring/`, `prometheus.yml` - Observability config.

Request flow: route -> service -> (rag components | OpenRouter) -> response.
Put new logic in a service, not in a route.

## Commands

Run everything from the repository root.
Imports use the `app.` package prefix, and paths like `app/uploads` and `app/vector_db` are relative to the root.

```bash
# Setup (Python 3.12, matching the Dockerfile)
python3.12 -m venv .venv && source .venv/bin/activate
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt

# Run the API locally
uvicorn app.main:app --reload        # Swagger UI at http://localhost:8000/docs

# Run the full stack (API, Redis, Prometheus, Grafana)
docker compose up

# Tests
python -m pytest app/tests

# Tests without a local venv, using the built image with the current code mounted
docker run --rm -v "$PWD/app:/app/app" aqili31/rag-app python -m pytest app/tests
```

The full test suite takes about 6 minutes on the owner's laptop.

There is no linter or formatter configured yet.

## Configuration

- Settings come from environment variables `OPENROUTER_API_KEY` and `OPENROUTER_MODEL` (see `sample.env`).
- `load_dotenv()` is commented out in `app/core/config.py`, so a local `.env` is not loaded automatically.
  Docker Compose loads it via `env_file`; for local runs, export the variables first.
- Never commit `.env` or print the API key.

## Gotchas

- Redis is optional. `REDIS_HOST` defaults to `redis`, which only resolves inside Docker Compose; set `REDIS_HOST=localhost` for local runs.
  If Redis is unreachable, `/ask-doc` still answers without the cache and Redis is skipped for 30 seconds before retrying.
  Always go through `cache_get` and `cache_set` in `app/core/cache.py`, never `redis_client` directly.
- The README's "cd app; uvicorn main:app" instruction is outdated and breaks the `app.` imports. Use the root command above.
- `app/uploads/` and `app/vector_db/` are runtime data, git-ignored and mounted as Docker volumes. Don't commit them.
- The Docker image installs CPU-only PyTorch on purpose to keep it small. Don't switch it to the default CUDA build.

## Testing conventions

- Tests use FastAPI's `TestClient` and mock the service function where the route imports it, e.g. `@patch("app.routes.rag.ask_document", new_callable=AsyncMock)`.
- Tests must not call OpenRouter, Redis or the vector store for real. Mock them.
- Add a test for every new endpoint and for every bug fix.

## Files to leave alone

- `memo.md` holds the owner's personal notes. Don't edit it unless asked.
- `README_comprehensive.md` is long-form documentation; update it only when the change affects what it describes.
