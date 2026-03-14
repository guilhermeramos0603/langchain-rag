from pydantic import BaseModel


class DebugRequest(BaseModel):
    code: str
    language: str = "python"


class DebugMetadata(BaseModel):
    latency_ms: float
    total_tokens: int
    model: str
    implementation: str = "langgraph"


class DebugResponse(BaseModel):
    bug_found: bool
    explanation: str
    fix: str
    test: str
    metadata: DebugMetadata
