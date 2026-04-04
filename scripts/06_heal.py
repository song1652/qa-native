"""
Step 6 — Healer: 실패 테스트 자동 분석
LLM 없음. pytest를 상세 모드로 재실행해 실패 정보를 수집, state.json에 저장.
Claude Code가 heal_context를 읽고 test_generated.py를 직접 패치한 뒤 05_execute.py를 재실행한다.

종료 코드:
  EXIT_SUCCESS (0) = 모든 테스트 통과 (힐링 불필요)
  EXIT_HEAL_NEEDED (1) = 실패 정보 저장 완료 → Claude Code가 패치 필요
  EXIT_HEAL_EXCEEDED (2) = 최대 힐링 횟수 초과 (기본 3회) → 파이프라인 중단
"""
import re
import subprocess
import sys
from pathlib import Path
from datetime import datetime
from _python import PYTHON_EXE
from _paths import PIPELINE_STATE, read_state, write_state
from _constants import EXIT_SUCCESS, EXIT_HEAL_NEEDED, EXIT_HEAL_EXCEEDED
from heal_utils import (
    classify_error, extract_key_lines,  # noqa: F401 (re-export for tests)
    find_screenshot_for_test, append_lessons, update_heal_stats,
)

MAX_HEAL = 3


def parse_failures(output: str, file_path: str) -> list[dict]:
    """pytest --tb=long 출력에서 실패 케이스별 정보를 추출한다.

    두 가지 패턴으로 수집:
    1. FAILED 줄에서 test_id/test_name 추출
    2. '_ test_name _' 구분선과 'FAILED' 줄 사이의 traceback 블록 매칭
    """
    failures = []

    # 패턴 1: '_ test_xxx _' ~ 'FAILED ...' 사이 traceback 블록 수집
    lines = output.splitlines()
    current = None
    for line in lines:
        # traceback 블록 시작: _____ test_xxx _____
        if re.match(r'^_{3,}\s+(test_\w+)\s+_{3,}$', line.strip()):
            match = re.match(r'^_{3,}\s+(test_\w+)\s+_{3,}$', line.strip())
            current = {"test_id": "", "test_name": match.group(1), "traceback": []}
            continue

        # FAILED 줄: 블록 종료 + test_id 업데이트
        if line.startswith("FAILED ") and "::" in line:
            test_id = line.split("FAILED ", 1)[1].strip()
            test_name = test_id.split("::")[-1]
            if current and current["test_name"] == test_name:
                current["test_id"] = test_id
                current["traceback"] = "\n".join(current["traceback"])
                failures.append(current)
                current = None
            elif current:
                current["traceback"] = "\n".join(current["traceback"])
                failures.append(current)
                current = None
                failures.append({"test_id": test_id, "test_name": test_name, "traceback": ""})
            else:
                failures.append({"test_id": test_id, "test_name": test_name, "traceback": ""})
            continue

        # '= short test summary info =' 줄 이후는 수집 중단
        if "short test summary info" in line:
            if current:
                current["traceback"] = "\n".join(current["traceback"])
                failures.append(current)
                current = None
            continue

        if current is not None:
            current["traceback"].append(line)

    if current:
        current["traceback"] = "\n".join(current["traceback"])
        failures.append(current)

    return failures


def collect_failure_details(file_path: str) -> tuple[list[dict], str]:
    """pytest를 상세 모드로 실행해 실패 정보를 수집한다."""
    try:
        result = subprocess.run(
            [PYTHON_EXE, "-m", "pytest", file_path, "--tb=long", "-v", "--no-header"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=300,  # 5분 타임아웃 (무한 행 방지)
        )
        output = result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        output = "[06] pytest 실행 타임아웃 (300초 초과)"
    failures = parse_failures(output, file_path)

    # 실패 케이스별 DOM 스냅샷 수집 (selector 힌트용)
    # 스크린샷은 conftest.py의 pytest_runtest_makereport 훅이 처리
    return failures, output


def main():
    state_path = PIPELINE_STATE
    if not state_path.exists():
        print("[오류] state/pipeline.json 없음.")
        sys.exit(1)

    state = read_state(state_path)

    execution_result = state.get("execution_result", {})
    if execution_result.get("failed", 0) == 0 and execution_result.get("exit_code", 1) == 0:
        print("[06] 모든 테스트 통과 - 힐링 불필요.")
        sys.exit(EXIT_SUCCESS)

    # 힐링 횟수 확인
    heal_count = state.get("heal_count", 0)
    if heal_count >= MAX_HEAL:
        print(f"[06] 최대 힐링 횟수({MAX_HEAL}회) 초과. 파이프라인을 중단합니다.")
        state["step"] = "heal_failed"
        write_state(state_path, state)
        sys.exit(EXIT_HEAL_EXCEEDED)

    # 힐링 전 사이트 접근 가능 체크
    url = state.get("url", "")
    if url:
        import urllib.request
        import urllib.error
        try:
            req = urllib.request.Request(url, method="HEAD")
            resp = urllib.request.urlopen(req, timeout=10)
            status = resp.getcode()
            if status >= 400:
                print(f"[06] 사이트 접근 불가: {url} (HTTP {status})")
                print("     사이트가 다운되었거나 접근이 차단되었습니다. 힐링을 건너뜁니다.")
                state["step"] = "heal_failed"
                state["heal_context"] = {"error": f"사이트 접근 불가 HTTP {status}", "url": url}
                write_state(state_path, state)
                sys.exit(EXIT_HEAL_EXCEEDED)
        except (urllib.error.URLError, OSError) as e:
            print(f"[06] 사이트 접근 불가: {url} ({e})")
            print("     사이트가 다운되었거나 네트워크 문제입니다. 힐링을 건너뜁니다.")
            state["step"] = "heal_failed"
            state["heal_context"] = {"error": f"사이트 접근 불가: {e}", "url": url}
            write_state(state_path, state)
            sys.exit(EXIT_HEAL_EXCEEDED)

    file_path = state.get("generated_file_path", "tests/generated/test_generated.py")
    if not Path(file_path).exists():
        print(f"[오류] 테스트 파일 없음: {file_path}")
        sys.exit(1)

    print(f"[06] 실패 분석 중 (힐링 {heal_count + 1}/{MAX_HEAL}회차)...")
    print()

    failures, raw_output = collect_failure_details(file_path)

    # 실패가 파싱되지 않은 경우 raw 출력 전체 저장
    if not failures and execution_result.get("exit_code", 0) != 0:
        failures = [{"test_id": "unknown", "test_name": "unknown", "traceback": raw_output[-3000:]}]

    # 각 failure에 스크린샷 경로 연결 (힐링 시 시각 검증용)
    for f in failures:
        f["screenshot"] = find_screenshot_for_test(f["test_name"])

    heal_context = {
        "heal_count": heal_count + 1,
        "failure_count": len(failures),
        "failures": failures,
        "url": state.get("url", ""),
        "raw_tail": raw_output[-2000:],  # 마지막 2000자 (Claude Code 참고용)
        "analyzed_at": datetime.now().isoformat(),
    }

    state["heal_context"] = heal_context
    state["heal_count"] = heal_count + 1
    state["step"] = "heal_needed"
    write_state(state_path, state)

    # 실수 패턴 자동 기록
    append_lessons(failures)

    # heal_stats.json 빈도 카운터 업데이트
    update_heal_stats(failures)

    print(f"[06] 실패 케이스: {len(failures)}건")
    print()
    for i, f in enumerate(failures, 1):
        print(f"  [{i}] {f['test_name']}")
        # 트레이스백에서 핵심 에러 라인만 출력
        tb_lines = f["traceback"].splitlines()
        error_lines = [l for l in tb_lines if "Error" in l or "assert" in l.lower() or "expect" in l.lower()]
        for el in error_lines[:3]:
            print(f"       {el.strip()}")
        print()

    print("=" * 60)
    print("  [Healer] Claude Code에 전달할 지시")
    print("=" * 60)
    print(f"  heal_context의 failures를 읽고")
    if Path(file_path).is_dir():
        print(f"  각 실패 파일을 직접 수정하세요:")
        seen = set()
        for f in failures:
            tid = f.get("test_id", "")
            if "::" in tid:
                fpath = tid.split("::")[0]
                if fpath not in seen:
                    seen.add(fpath)
                    print(f"    - {fpath}")
    else:
        print(f"  {file_path} 를 직접 수정하세요.")
    print()
    print("  수정 기준:")
    print("  1. Locator 오류 → dom_info의 셀렉터와 대조해 수정")
    print("  2. Assertion 오류 → 실제 페이지 텍스트/상태로 기댓값 수정")
    print("  3. Timeout → wait_for_selector 또는 expect timeout 조정")
    print("  4. MCP 시각 검증 → 원인 불명확 시 Playwright MCP로 실제 페이지 확인")
    print()
    print("  수정 후: python scripts/05_execute.py → python scripts/06_heal.py 순으로 재실행")
    print("=" * 60)
    sys.exit(EXIT_HEAL_NEEDED)


if __name__ == "__main__":
    main()
