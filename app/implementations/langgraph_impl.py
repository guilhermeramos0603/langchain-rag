from typing import TypedDict

from langgraph.graph import StateGraph, END
from openai import OpenAI

from app.rag.retriever import retrieve
from app.utils.metrics import MetricsTracker


class DebugState(TypedDict):
    code: str
    language: str
    parsed_context: str
    rag_context: str
    bug_explanation: str
    fix: str
    test: str
    metrics: MetricsTracker


MODEL = "gpt-4o-mini"


def _call_llm(client: OpenAI, system: str, user: str, metrics: MetricsTracker) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=0.2,
    )
    usage = response.usage
    if usage:
        metrics.add_tokens(usage.prompt_tokens, usage.completion_tokens)
    metrics.model = MODEL
    return response.choices[0].message.content or ""


def parse_code(state: DebugState) -> dict:
    client = OpenAI()
    result = _call_llm(
        client,
        system="You are a code analyst. Describe what this code does, its structure, and any potential issues. Be concise.",
        user=f"Language: {state['language']}\n\nCode:\n```\n{state['code']}\n```",
        metrics=state["metrics"],
    )
    return {"parsed_context": result}


def identify_bug(state: DebugState) -> dict:
    client = OpenAI()
    rag_docs = retrieve(f"{state['language']} bug: {state['code'][:200]}")
    rag_context = "\n---\n".join(rag_docs)

    result = _call_llm(
        client,
        system=(
            "You are an expert debugger. Given the code analysis and reference documentation about common errors, "
            "identify the bug in the code. Explain clearly what the bug is and why it causes problems."
        ),
        user=(
            f"Code analysis:\n{state['parsed_context']}\n\n"
            f"Reference documentation on common errors:\n{rag_context}\n\n"
            f"Original code:\n```{state['language']}\n{state['code']}\n```"
        ),
        metrics=state["metrics"],
    )
    return {"bug_explanation": result, "rag_context": rag_context}


def generate_fix(state: DebugState) -> dict:
    client = OpenAI()
    result = _call_llm(
        client,
        system=(
            "You are an expert programmer. Given the bug explanation, provide the corrected code. "
            "Return ONLY the corrected code, no explanations."
        ),
        user=(
            f"Bug explanation:\n{state['bug_explanation']}\n\n"
            f"Original code:\n```{state['language']}\n{state['code']}\n```"
        ),
        metrics=state["metrics"],
    )
    return {"fix": result}


def write_test(state: DebugState) -> dict:
    client = OpenAI()
    result = _call_llm(
        client,
        system=(
            f"You are a test engineer. Write a test in {state['language']} that would catch "
            "the original bug. The test should pass with the fixed code and fail with the buggy code. "
            "Return ONLY the test code."
        ),
        user=(
            f"Bug explanation:\n{state['bug_explanation']}\n\n"
            f"Buggy code:\n```{state['language']}\n{state['code']}\n```\n\n"
            f"Fixed code:\n```{state['language']}\n{state['fix']}\n```"
        ),
        metrics=state["metrics"],
    )
    return {"test": result}


def build_graph() -> StateGraph:
    graph = StateGraph(DebugState)

    graph.add_node("parse_code", parse_code)
    graph.add_node("identify_bug", identify_bug)
    graph.add_node("generate_fix", generate_fix)
    graph.add_node("write_test", write_test)

    graph.set_entry_point("parse_code")
    graph.add_edge("parse_code", "identify_bug")
    graph.add_edge("identify_bug", "generate_fix")
    graph.add_edge("generate_fix", "write_test")
    graph.add_edge("write_test", END)

    return graph.compile()


async def run_debug(code: str, language: str) -> dict:
    graph = build_graph()
    metrics = MetricsTracker()

    initial_state: DebugState = {
        "code": code,
        "language": language,
        "parsed_context": "",
        "rag_context": "",
        "bug_explanation": "",
        "fix": "",
        "test": "",
        "metrics": metrics,
    }

    result = graph.invoke(initial_state)

    return {
        "bug_found": bool(result["bug_explanation"]),
        "explanation": result["bug_explanation"],
        "fix": result["fix"],
        "test": result["test"],
        "metadata": {
            "latency_ms": round(metrics.latency_ms, 2),
            "total_tokens": metrics.total_tokens,
            "model": metrics.model,
            "implementation": "langgraph",
        },
    }
