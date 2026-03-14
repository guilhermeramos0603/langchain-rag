import json
import time
from pathlib import Path

import httpx

BUG_CASES_FILE = Path(__file__).parent / "bug_cases" / "cases.json"
RESULTS_DIR = Path(__file__).parents[1] / "results"
BASE_URL = "http://localhost:8000"


def load_cases() -> list[dict]:
    return json.loads(BUG_CASES_FILE.read_text())


def run_all_cases():
    cases = load_cases()
    results = []

    with httpx.Client(timeout=120.0) as client:
        for case in cases:
            print(f"\n--- Running: {case['id']} ---")
            start = time.time()

            try:
                response = client.post(
                    f"{BASE_URL}/debug/langgraph",
                    json={"code": case["code"], "language": case["language"]},
                )
                response.raise_for_status()
                data = response.json()

                result = {
                    "case_id": case["id"],
                    "expected_bug": case["expected_bug"],
                    "bug_found": data["bug_found"],
                    "explanation": data["explanation"],
                    "fix": data["fix"],
                    "test": data["test"],
                    "metadata": data["metadata"],
                    "total_time_ms": round((time.time() - start) * 1000, 2),
                    "status": "success",
                }
            except Exception as e:
                result = {
                    "case_id": case["id"],
                    "status": "error",
                    "error": str(e),
                    "total_time_ms": round((time.time() - start) * 1000, 2),
                }

            results.append(result)
            print(f"  Status: {result['status']}")
            if result["status"] == "success":
                print(f"  Bug found: {result['bug_found']}")
                print(f"  Latency: {result['metadata']['latency_ms']}ms")
                print(f"  Tokens: {result['metadata']['total_tokens']}")

    RESULTS_DIR.mkdir(exist_ok=True)
    output_file = RESULTS_DIR / "langgraph_results.json"
    output_file.write_text(json.dumps(results, indent=2))
    print(f"\nResults saved to {output_file}")

    successful = sum(1 for r in results if r["status"] == "success")
    bugs_found = sum(1 for r in results if r.get("bug_found"))
    print(f"\nSummary: {successful}/{len(cases)} successful, {bugs_found} bugs found")


if __name__ == "__main__":
    run_all_cases()
