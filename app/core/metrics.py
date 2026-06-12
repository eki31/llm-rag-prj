from prometheus_client import Counter, Histogram

#Total API Requests
REQUEST_COUNT = Counter("api_requests_total","Total API Requests")

#Request Latency
REQUEST_LATENCY = Histogram("api_request_latency_seconds","Request Latency")

#RAG Requests
RAG_REQUEST_COUNT = Counter("rag_requests_total","Total Rag Requests")

#Cache Hits
CACHE_HITS = Counter("cache_hits_total","Cache Hits")

#Cache Misses
CACHE_MISSES = Counter("cache_misses_total", "Cache Misses")

DOCUMENT_UPLOADS = Counter("document_upload_total","Total uploaded documents")

OPENROUTER_CALLS = Counter("llm_requests_total","Total LLM requests")

VECTOR_INGESTIONS = Counter("vector_ingestions_total","Total vector ingestions")