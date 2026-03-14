import os

from dotenv import load_dotenv
from fastapi import FastAPI

from app.models import DebugRequest, DebugResponse
from app.implementations.langgraph_impl import run_debug

load_dotenv()

app = FastAPI(title="AI Debug Battle", version="0.1.0")


@app.post("/debug/langgraph", response_model=DebugResponse)
async def debug_langgraph(request: DebugRequest):
    result = await run_debug(request.code, request.language)
    return DebugResponse(**result)


@app.get("/health")
async def health():
    return {"status": "ok"}
