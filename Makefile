.PHONY: setup run index test health clean

setup:
	python3 -m venv .venv
	.venv/bin/pip install -e .
	cp -n .env.example .env || true
	@echo "Done! Edit .env with your OPENAI_API_KEY"

run:
	.venv/bin/uvicorn app.main:app --reload

index:
	.venv/bin/python -m app.rag.indexer

test:
	.venv/bin/python -m tests.test_runner

health:
	curl -s http://localhost:8000/health | python3 -m json.tool

debug-example:
	curl -s -X POST http://localhost:8000/debug/langgraph \
		-H "Content-Type: application/json" \
		-d '{"code": "def get_item(lst, idx): return lst[idx+1]", "language": "python"}' \
		| python3 -m json.tool

clean:
	rm -rf chroma_db/ results/*.json __pycache__ .pytest_cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
