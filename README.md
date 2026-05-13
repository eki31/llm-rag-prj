
# Phase 1 Project : AI Knowledge Assistant API

A production-style AI backend API built with **FastAPI**, integrated with **OpenRouter LLM APIs**, containerized using **Docker**, and enhanced with asynchronous request handling, structured logging, and unit testing.

This project was built as part of my MLOps learning roadmap to strengthen backend engineering, API development, Docker, and production engineering fundamentals before progressing into RAG systems and Kubernetes deployment.

---

# Features

## Core Features

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
Send a question to an LLM through OpenRouter.

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

# Tech Stack

- **Python**
- **FastAPI**
- **Uvicorn**
- **OpenRouter API**
- **HTTPX (async requests)**
- **Pydantic**
- **Docker**
- **Pytest**
- **Python Dotenv**

---

# Architecture

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

# Project Structure

```text
ai-knowledge-api/
│
├── app/
│   ├── main.py
│   │
│   ├── routes/
│   │   └── ai.py
│   │
│   ├── services/
│   │   ├── openrouter_service.py
│   │   └── response_formatter.py
│   │
│   ├── models/
│   │   └── schemas.py
│   │
│   └── core/
│       ├── config.py
│       └── logger.py
│
├── tests/
│   ├── test_health.py
│   └── test_ask.py
│
├── .env
├── requirements.txt
├── Dockerfile
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

Through this project, I practiced:

- Backend API development
- FastAPI fundamentals
- REST API design
- Asynchronous programming
- Docker containerization
- Structured logging
- Error handling
- Unit testing
- Production-style project structure

---

# Future Improvements

Planned enhancements:

- API authentication
- Rate limiting
- Request tracing / request IDs
- CI/CD pipeline
- Kubernetes deployment
- RAG integration
- Monitoring with Prometheus/Grafana


# Phase 2 Project : Production-style RAG System.

RAG flow

PDF Upload
      ↓
Document Loader
      ↓
Text Splitter
(chunking)
      ↓
Embedding Model
      ↓
ChromaDB
(store vectors)
      ↓
Retriever
      ↓
Question
      ↓
Retrieved Context
      ↓
OpenRouter LLM
      ↓
Answer + Sources