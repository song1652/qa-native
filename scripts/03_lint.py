"""
Step 3 — 코드 lint 검사
LLM 없음. flake8 실행 후 결과를 state.json에 저장.
Claude Code는 결과를 보고 QA 리드용 요약을 직접 작성한다.
"""
import json
import subprocess
import sys
from pathlib import Path


def main():
    state_path = Path("state.json")
    if not state_path.exists():
        print("[오류] state.json 없음.")
        sys.exit(1)

    state = json.loads(state_path.read_text(encoding="utf-8"))
    file_path = state.get("generated_file_path", "tests/generated/test_generated.py")

    if not Path(file_path).exists():
        print(f"[오류] 테스트 파일 없음: {file_path}")
        sys.exit(1)

    print(f"[03] lint 검사 중: {file_path}")

    result = subprocess.run(
        [sys.executable, "-m", "flake8", file_path, "--max-line-length=120", "--statistics"],
        capture_output=True, text=True
    )

    issues_raw = result.stdout.strip()
    issue_lines = [l for l in issues_raw.splitlines() if l.strip()]

    lint_result = {
        "passed":      result.returncode == 0,
        "issue_count": len([l for l in issue_lines if file_path in l]),
        "issues":      issues_raw if issues_raw else "이슈 없음",
        "file":        file_path,
    }

    state["lint_result"] = lint_result
    state["step"] = "linted"
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

    status = "통과" if lint_result["passed"] else f"이슈 {lint_result['issue_count']}건"
    print(f"[03] lint {status}")
    if not lint_result["passed"]:
        print(lint_result["issues"])

    print()
    print("[다음] Claude Code가 코드 + lint 결과를 보고 QA 리드용 요약을 작성합니다.")


if __name__ == "__main__":
    main()
