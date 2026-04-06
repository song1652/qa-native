"""
병렬 파이프라인 Step 99 - 실행 + 통합 리포트

1. tests/generated/ 에서 pytest 일괄 실행 (JSON 리포트)
2. 실패 시 heal_context 저장 → Claude Code 힐링 루프 (최대 3회)
3. 그룹별 PASS/FAIL 집계
4. HTML 리포트 생성 (tests/reports/parallel_index_{ts}.html)

LLM 없음. 순수 Python.
"""
import ast
import json
import shutil
import subprocess
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict

_SCRIPTS_DIR = str(Path(__file__).parent.parent / "scripts")
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)
from _paths import (
    PROJECT_ROOT, PARALLEL_STATE, HEAL_CONTEXT_STATE, QUICK_STATE,
    read_state, write_state, append_run_history,
)
from _python import PYTHON_EXE
from heal_utils import (
    classify_error, extract_key_lines,
    find_screenshot_for_test, append_lessons,
    LESSONS_PATH,
)
from report_html import case_row as _case_row, build_report
from result_parser import parse_results
try:
    from parse_cases import load_cases as _load_cases
except ImportError:
    _load_cases = None

GENERATED_DIR = PROJECT_ROOT / "tests" / "generated"
TESTCASES_DIR = PROJECT_ROOT / "testcases"
SCREENSHOTS_DIR = PROJECT_ROOT / "tests" / "screenshots"
MAX_HEAL = 3


# ── 상태 업데이트 헬퍼 ──────────────────────────────────────────


def _update_parallel_status(status: str, extra: dict | None = None) -> None:
    """state/parallel.json의 status 필드를 업데이트 (기존 데이터 보존)."""
    state = read_state(PARALLEL_STATE)
    state["status"] = status
    if extra:
        state.update(extra)
    write_state(PARALLEL_STATE, state)


# ── pytest 실행 ──────────────────────────────────────────────────


def build_heal_context(report: dict, heal_count: int) -> dict | None:
    """실패 테스트의 traceback을 모아 heal_context.json 생성. 실패 없으면 None 반환."""
    failures = []
    for t in report.get("tests", []):
        if t.get("outcome") in ("failed", "error"):
            call = t.get("call") or {}
            longrepr = call.get("longrepr", "")
            if isinstance(longrepr, dict):
                longrepr = longrepr.get("reprcrash", {}).get("message", str(longrepr))
            test_name = t.get("nodeid", "").split("::")[-1]
            failures.append({
                "test_id": t.get("nodeid", ""),
                "test_name": test_name,
                "file": t.get("nodeid", "").split("::")[0],
                "traceback": str(longrepr),
                "screenshot": find_screenshot_for_test(test_name),
            })
    if not failures:
        return None

    # 실패 그룹의 URL 수집 (pages.json에서)
    urls = {}
    pages_path = PROJECT_ROOT / "config" / "pages.json"
    if pages_path.exists():
        try:
            pages_data = json.loads(pages_path.read_text(encoding="utf-8"))
            for f in failures:
                group = f["file"].split("/")[-2] if "/" in f["file"] else None
                if group and group in pages_data and group not in urls:
                    urls[group] = pages_data[group]
        except Exception:
            pass

    ctx = {
        "heal_count": heal_count,
        "failure_count": len(failures),
        "failures": failures,
        "urls": urls,
        "analyzed_at": datetime.now().isoformat(),
    }
    write_state(HEAL_CONTEXT_STATE, ctx)
    print(f"\n[99] heal_context 저장됨: {HEAL_CONTEXT_STATE}  ({len(failures)}건 실패)")

    # 실수 패턴 자동 기록
    append_lessons(failures)

    return ctx


def print_heal_instructions(heal_context: dict) -> None:
    """Claude Code가 힐링할 수 있도록 컨텍스트를 stdout에 출력."""
    print("\n" + "=" * 60)
    print("  테스트 실패 — 힐링 필요")
    print("=" * 60)
    print(f"  heal_count : {heal_context['heal_count']} / {MAX_HEAL}")
    print(f"  failures   : {heal_context['failure_count']}건")
    print()
    for f in heal_context["failures"]:
        print(f"  [{f['test_name']}]")
        lines = f["traceback"].splitlines()[:10]
        for line in lines:
            print(f"    {line}")
        print()
    print(f"  heal_context 저장: {HEAL_CONTEXT_STATE}")
    print()
    # MCP 시각 검증 안내
    screenshots = [f for f in heal_context["failures"] if f.get("screenshot")]
    if screenshots:
        print(f"  스크린샷: {len(screenshots)}개 (Read tool로 시각 확인 가능)")
        print()
    print("  Claude Code는 위 traceback을 보고 해당 테스트 파일을 패치한 후")
    print("  python parallel/99_merge.py 를 다시 실행하세요.")
    print()
    print("  [MCP 시각 검증] 원인 불명확 시 Playwright MCP로 실제 페이지 확인 가능")
    print()
    print("  [필수] 힐링 완료 체크리스트:")
    print("    1. 코드 패치 적용")
    print("    2. agents/lessons_learned.md에 힐링 기록 추가")
    print("    3. python parallel/99_merge.py 재실행으로 통과 확인")
    print("=" * 60)


def verify_lessons_learned_updated(heal_start_time: str) -> bool:
    """힐링 후 lessons_learned.md가 업데이트되었는지 검증.

    heal_start_time 이후에 lessons_learned.md가 수정되었는지 확인.
    누락 시 경고 출력, 반환값은 업데이트 여부.
    """
    if not LESSONS_PATH.exists():
        return False
    from datetime import datetime as dt
    try:
        start = dt.fromisoformat(heal_start_time)
        mtime = dt.fromtimestamp(LESSONS_PATH.stat().st_mtime)
        if mtime > start:
            return True
    except Exception:
        pass
    print()
    print("⚠ [경고] lessons_learned.md 기록이 누락되었습니다!")
    print("  힐링 패치 후 반드시 agents/lessons_learned.md에 기록해야 합니다.")
    print("  형식: ### [힐링] {날짜} — {파일명}")
    print("        - **문제**: {traceback 요약}")
    print("        - **수정**: {적용한 패치 내용}")
    print("        - **재발 방지**: {동일 실수 방지 규칙}")
    print()
    return False


# ── HTML 리포트 ──────────────────────────────────────────────────


def _load_cases_for_group(group_name: str) -> list:
    """testcases/{group_name}/ 에서 케이스 메타데이터 로드."""
    if not _load_cases:
        return []
    group_dir = TESTCASES_DIR / group_name
    if group_dir.is_dir():
        return _load_cases(str(group_dir))
    return []


def _scan_generated_groups() -> dict[str, list[Path]]:
    """tests/generated/ 하위 그룹별 파일 목록 반환."""
    groups: dict[str, list[Path]] = defaultdict(list)
    if not GENERATED_DIR.exists():
        return groups
    for group_dir in sorted(GENERATED_DIR.iterdir()):
        if not group_dir.is_dir() or group_dir.name.startswith("."):
            continue
        for f in sorted(group_dir.glob("*.py")):
            if f.name != "conftest.py" and f.name != "__init__.py":
                groups[group_dir.name].append(f)
    return groups


def build_html(test_results: dict, summary: dict,
               created_at: str, target_groups: list[str] | None = None) -> str:
    groups = _scan_generated_groups()
    if target_groups:
        groups = {k: v for k, v in groups.items() if k in target_groups}

    groups_data = []
    for label, files in groups.items():
        group_tests = {
            k: v for k, v in test_results.items()
            if f"/{label}/" in k or f"\\{label}\\" in k
        }
        g_pass_cnt = sum(1 for v in group_tests.values() if v)
        g_total_cnt = len(group_tests)
        g_passed = all(group_tests.values()) if group_tests else False

        cases = _load_cases_for_group(label)
        rows_html = ""
        if cases:
            for case_idx, case in enumerate(cases):
                uid = f"{label}_{case_idx}"
                case_pass = all(group_tests.values()) if group_tests else False
                rows_html += _case_row(case, uid, case_pass)
        else:
            for file_idx, f in enumerate(files):
                uid = f"{label}_{file_idx}"
                nodeid_match = next(
                    (k for k in test_results if f.stem in k), None
                )
                is_passed = test_results.get(nodeid_match, False) if nodeid_match else False
                simple_case = {
                    "title": f.stem.replace("_", " ").title(),
                    "precondition": "", "steps": [], "expected": "",
                }
                rows_html += _case_row(simple_case, uid, is_passed)

        if not rows_html:
            rows_html = '<p class="empty-msg">케이스 정보 없음</p>'

        groups_data.append({
            "label": label, "rows_html": rows_html,
            "pass_cnt": g_pass_cnt, "total_cnt": g_total_cnt,
            "all_pass": g_passed, "has_tests": bool(group_tests),
        })

    return build_report(groups_data, summary, created_at, "Parallel Test Report")


# ── 메인 ────────────────────────────────────────────────────────


def main():
    import argparse
    import tempfile
    parser = argparse.ArgumentParser(description="QA 테스트 실행 + 리포트 생성")
    parser.add_argument(
        "--group", "-g",
        nargs="*",
        metavar="FOLDER",
        help="실행할 폴더명 (예: login checkout). 생략 시 전체 실행."
    )
    parser.add_argument(
        "--quick", action="store_true",
        help="빠른 실행 모드: state/quick.json에 결과 저장 (parallel_state 미변경)"
    )
    parser.add_argument(
        "--no-heal", action="store_true",
        help="힐링 단계 생략: 실패해도 heal_context를 생성하지 않음"
    )
    args = parser.parse_args()
    import time as _time
    _start_time = _time.monotonic()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 1. 실행 대상 결정
    if args.group:
        target_dirs = [GENERATED_DIR / g for g in args.group]
        missing = [str(d) for d in target_dirs if not d.exists()]
        if missing:
            print(f"[오류] 존재하지 않는 폴더: {', '.join(missing)}")
            available = [d.name for d in GENERATED_DIR.iterdir() if d.is_dir()]
            print(f"  사용 가능한 폴더: {', '.join(available) or '없음'}")
            return
        existing = []
        for d in target_dirs:
            existing.extend(f for f in d.rglob("*.py") if f.name != "conftest.py")
        scope_label = ", ".join(args.group)
    else:
        existing = [f for f in GENERATED_DIR.rglob("*.py") if f.name != "conftest.py"] if GENERATED_DIR.exists() else []
        scope_label = "전체"

    if not existing:
        print("[오류] 실행할 테스트 파일 없음.")
        if GENERATED_DIR.exists():
            available = [d.name for d in GENERATED_DIR.iterdir() if d.is_dir()]
            if available:
                print(f"  사용 가능한 폴더: {', '.join(available)}")
                print(f"  예시: python parallel/99_merge.py --group {available[0]}")
        return

    n_workers = min(len(existing), 8)

    # 의존성 있는 테스트 감지
    has_dependent = any(
        len([n for n in ast.parse(f.read_text(encoding="utf-8")).body
             if isinstance(n, ast.FunctionDef) and n.name.startswith("test_")]) > 1
        for f in existing
    )
    dist_mode = "loadfile" if has_dependent else "load"

    print(f"\n[99] 실행 범위: {scope_label}  ({len(existing)}개 파일)")
    print(f"[99] 병렬 실행: workers={n_workers}  dist={dist_mode}"
          + (" (의존 테스트 감지 → loadfile)" if has_dependent else ""))

    # 기존 heal_context 읽기 (재실행 시 heal_count 이어받기)
    heal_count = 0
    heal_analyzed_at = None
    prev = read_state(HEAL_CONTEXT_STATE)
    if prev:
        heal_count = prev.get("heal_count", 0)
        heal_analyzed_at = prev.get("analyzed_at")

    # 힐링 재실행 시 lessons_learned 기록 검증
    if heal_count > 0 and heal_analyzed_at:
        verify_lessons_learned_updated(heal_analyzed_at)

    # pytest 대상 경로
    if args.group:
        test_targets = [str(GENERATED_DIR / g) for g in args.group]
    else:
        test_targets = [str(GENERATED_DIR)]

    # 2. pytest 실행 전 스크린샷 정리 (최종 실패 시만 남기기)
    if SCREENSHOTS_DIR.exists():
        shutil.rmtree(SCREENSHOTS_DIR, ignore_errors=True)

    # --quick 플래그만 quick mode (state/quick.json 사용)
    # --group 단독 사용 시에는 parallel.json 업데이트
    quick_mode = args.quick
    state_path = QUICK_STATE if quick_mode else PARALLEL_STATE

    if not quick_mode:
        _update_parallel_status("testing")

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_report_path = Path(tempfile.gettempdir()) / f"qa_report_{ts}.json"

    try:
        proc = subprocess.run(
            [PYTHON_EXE, "-m", "pytest"] + test_targets + [
                f"-n{n_workers}",
                f"--dist={dist_mode}",
                "--json-report",
                f"--json-report-file={json_report_path}",
                "--tb=short", "-v",
            ],
            cwd=str(PROJECT_ROOT),
            capture_output=False,
            timeout=900,
        )
        pytest_exit_code = proc.returncode
    except subprocess.TimeoutExpired:
        print("\n[99] pytest 실행 타임아웃 (900초 초과)")
        pytest_exit_code = -1
    report = {}
    if json_report_path.exists():
        report = json.loads(json_report_path.read_text(encoding="utf-8"))
        json_report_path.unlink()

    # 3. 결과 파싱
    test_results = parse_results(report)
    pytest_summary = report.get("summary", {})

    # 3-b. 실패 판정: pytest 종료코드 + JSON 리포트 모두 확인
    #      collection error 등은 JSON summary에 안 잡히므로 종료코드로 보완
    failed_count = pytest_summary.get("failed", 0) + pytest_summary.get("error", 0)
    has_issues = pytest_exit_code != 0 or failed_count > 0
    if has_issues:
        if args.no_heal:
            print(f"\n[99] 실패 {failed_count}건 — 힐링 생략 (--no-heal)")
            HEAL_CONTEXT_STATE.unlink(missing_ok=True)
        elif heal_count >= MAX_HEAL:
            print(f"\n[99] 최대 힐링 횟수({MAX_HEAL}회) 초과 — 수동 수정이 필요합니다.")
            HEAL_CONTEXT_STATE.unlink(missing_ok=True)
        else:
            heal_count += 1
            heal_ctx = build_heal_context(report, heal_count)
            if heal_ctx:
                print_heal_instructions(heal_ctx)
    else:
        HEAL_CONTEXT_STATE.unlink(missing_ok=True)

    # 4. HTML 리포트 (힐링 완료 후에만 생성: 전체 통과 또는 최대 힐링 초과)
    is_final_run = (not has_issues) or heal_count >= MAX_HEAL or args.no_heal
    index_path = None
    if is_final_run:
        report_dir = PROJECT_ROOT / "tests" / "reports"
        report_dir.mkdir(parents=True, exist_ok=True)
        index_path = report_dir / f"parallel_index_{ts}.html"
        index_path.write_text(
            build_html(test_results, pytest_summary, now,
                       target_groups=args.group),
            encoding="utf-8"
        )

    # 5. state/parallel.json (또는 quick.json)에 실행 결과 저장
    passed = pytest_summary.get("passed", 0)
    failed = pytest_summary.get("failed", 0) + pytest_summary.get("error", 0)
    total = passed + failed
    pass_rate = round(passed / total * 100, 1) if total else 0

    # 그룹별 결과 집계
    group_results = {}
    for nodeid, is_passed in test_results.items():
        parts = nodeid.split("/")
        group = None
        for i, p in enumerate(parts):
            if p == "generated" and i + 1 < len(parts):
                group = parts[i + 1]
                break
        if not group:
            continue
        if group not in group_results:
            group_results[group] = {"passed": 0, "failed": 0, "tests": []}
        if is_passed:
            group_results[group]["passed"] += 1
        else:
            group_results[group]["failed"] += 1
        group_results[group]["tests"].append({
            "nodeid": nodeid,
            "name": nodeid.split("::")[-1] if "::" in nodeid else nodeid,
            "passed": is_passed,
        })

    run_state = read_state(state_path)

    run_state["execution_result"] = {
        "passed": passed,
        "failed": failed,
        "total": total,
        "pass_rate": pass_rate,
        "report_path": str(index_path.relative_to(PROJECT_ROOT)) if index_path else None,
        "report_name": index_path.name if index_path else None,
        "group_results": group_results,
        "executed_at": now,
        "heal_count": heal_count,
    }
    if failed == 0:
        run_state["status"] = "done"
    elif args.no_heal:
        run_state["status"] = "done"
    elif heal_count >= MAX_HEAL:
        run_state["status"] = "heal_failed"
    else:
        run_state["status"] = "heal_needed"
    write_state(state_path, run_state)

    # 실행 이력 기록
    _duration = round(_time.monotonic() - _start_time, 1)
    groups_list = list(group_results.keys()) if group_results else (args.group or [])
    append_run_history({
        "timestamp": now,
        "pipeline": "quick" if quick_mode else "parallel",
        "groups": groups_list,
        "passed": passed,
        "failed": failed,
        "total": total,
        "pass_rate": pass_rate,
        "heal_count": heal_count,
        "first_pass": failed == 0 and heal_count == 0,
        "duration_sec": _duration,
    })

    # 6. 요약 출력
    print()
    print("=" * 60)
    print("  QA Report Generated")
    print("=" * 60)
    print(f"  Total  : {total}")
    print(f"  Passed : {passed}")
    print(f"  Failed : {failed}")
    print()
    print(f"  Tests  : {GENERATED_DIR}")
    print(f"  Report : {index_path or '(힐링 중 — 최종 실행 시 생성)'}")
    print("=" * 60)


if __name__ == "__main__":
    main()
