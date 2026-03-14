# AI Debug Battle

AI Debug Assistant comparing different implementation approaches, starting with LangGraph + RAG.

## Setup

```bash
# Install dependencies
uv sync

# Configure environment
cp .env.example .env
# Edit .env with your OPENAI_API_KEY

# Index RAG documents
uv run python -m app.rag.indexer
```

## Run

```bash
# Start the server
uv run uvicorn app.main:app --reload

# Test a single bug
curl -X POST http://localhost:8000/debug/langgraph \
  -H "Content-Type: application/json" \
  -d '{"code": "def get_item(lst, idx): return lst[idx+1]", "language": "python"}'

# Run all 10 bug cases
uv run python -m tests.test_runner
```

## Architecture (Phase 1 — LangGraph)

```
POST /debug/langgraph
  → parse_code (analyze code structure)
  → identify_bug (RAG context + LLM)
  → generate_fix (corrected code)
  → write_test (regression test)
```

RAG uses ChromaDB + OpenAI embeddings to provide context about common error patterns.
