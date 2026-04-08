"""
Step 5 — 테스트 실행
LLM 없음. pytest 실행 후 결과를 state.json에 저장.
"""
import ast
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime


def count_test_functions(file_path: str) -> tuple[int, bool]:
    """테스트 함수 수와 의존성 여부 반환."""
    try:
        tree = ast.parse(Path(file_path).read_text(encoding="utf-8"))
        funcs = [n for n in tree.body
                 if isinstance(n, ast.FunctionDef) and n.name.startswith("test_")]
        # 함수가 여러 개면 순서 의존 가능성 → loadfile
        return len(funcs), len(funcs) > 1
    except Exception:
        return 1, False


def main():
    state_path = Path("state.json")
    if not state_path.exists():
        print("[오류] state.json 없음.")
        sys.exit(1)

    state = json.loads(state_path.read_text(encoding="utf-8"))

    if state.get("approval_status") != "approved":
        print("[오류] 미승인 상태. 04_approve.py를 먼저 실행하세요.")
        sys.exit(1)

    file_path = state.get("generated_file_path", "tests/generated/test_generated.py")
    if not Path(file_path).exists():
        print(f"[오류] 테스트 파일 없음: {file_path}")
        sys.exit(1)

    # 리포트 경로
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = Path("tests/reports")
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = str(report_dir / f"report_{ts}.html")

    n_funcs, has_dependent = count_test_functions(file_path)
    parallel_opts = []
    if n_funcs > 1:
        dist_mode = "loadfile" if has_dependent else "load"
        n_workers = min(n_funcs, 4)
        parallel_opts = [f"-n{n_workers}", f"--dist={dist_mode}"]
        print(f"[05] 테스트 실행 중: {file_path}  ({n_funcs}개 함수, 병렬 workers={n_workers}, dist={dist_mode})")
    else:
        print(f"[05] 테스트 실행 중: {file_path}")
    print()

    result = subprocess.run(
        [
            sys.executable, "-m", "pytest", file_path,
            f"--html={report_path}",
            "--self-contained-html",
            "-v",
            "--tb=short",
        ] + parallel_opts,
        capture_output=False,   # 실시간 출력
        text=True,
    )

    # 결과 파싱 (재실행으로 요약만 수집)
    summary_result = subprocess.run(
        [sys.executable, "-m", "pytest", file_path, "--tb=no", "-q"],
        capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    summary_lines = [
        l for l in (summary_result.stdout or "").splitlines()
        if any(k in l for k in ("passed", "failed", "error", "warning"))
    ]
    summary = summary_lines[-1].strip() if summary_lines else "결과 없음"

    execution_result = {
        "passed":      result.returncode == 0,
        "exit_code":   result.returncode,
        "summary":     summary,
        "report_path": report_path,
        "executed_at": datetime.now().isoformat(),
    }

    state["execution_result"] = execution_result
    state["step"] = "done"
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

    print()
    print("=" * 55)
    status = "성공" if execution_result["passed"] else "실패"
    print(f"  테스트 {status}: {summary}")
    print(f"  HTML 리포트: {report_path}")
    print("=" * 55)


if __name__ == "__main__":
    main()
