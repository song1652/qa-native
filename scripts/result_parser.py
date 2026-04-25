"""pytest JSON 리포트 파싱 공통 모듈.

05_execute.py (단일)와 99_merge.py (병렬)가 공유.
"""


def parse_results(report: dict) -> dict:
    """JSON 리포트 → {nodeid: outcome} 매핑.

    outcome 값: "passed" | "failed" | "skipped"
    """
    results = {}
    for t in report.get("tests", []):
        nodeid = t.get("nodeid", "")
        outcome = t.get("outcome", "failed")
        if outcome not in ("passed", "skipped"):
            outcome = "failed"
        results[nodeid] = outcome
    return results
