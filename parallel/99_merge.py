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
    find_screenshot_for_test, append_lessons, update_heal_stats,
    build_heal_batches, print_heal_batches,
    LESSONS_PATH, LESSONS_AUTO_PATH,
)
from report_html import case_row as _case_row, build_report
from result_parser import parse_results
from structured_log import slog
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


def _check_urls_accessible(urls: dict) -> dict | None:
    """힐링 전 사이트 접근 가능 여부를 사전 체크. 접근 불가 시 에러 dict 반환."""
    import urllib.request
    import urllib.error
    for group, url in urls.items():
        if not url:
            continue
        try:
            req = urllib.request.Request(url, method="HEAD")
            resp = urllib.request.urlopen(req, timeout=10)
            if resp.getcode() >= 400:
                return {"error": f"사이트 접근 불가 HTTP {resp.getcode()}", "url": url, "group": group}
        except (urllib.error.URLError, OSError) as e:
            return {"error": f"사이트 접근 불가: {e}", "url": url, "group": group}
    return None


def _detect_repeated_failures_parallel(
    current_failures: list[dict], prev_ctx: dict
) -> tuple[list[dict], list[dict]]:
    """이전 heal_context와 비교하여 동일 (test_name, error_type) 반복 감지.

    Returns:
        (healable, skipped)
    """
    prev_failures = prev_ctx.get("failures", [])
    if not prev_failures:
        return current_failures, []

    prev_signatures = set()
    for f in prev_failures:
        etype = f.get("error_type") or classify_error(f.get("traceback", ""))
        prev_signatures.add((f.get("test_name", ""), etype))

    healable, skipped = [], []
    for f in current_failures:
        sig = (f.get("test_name", ""), f.get("error_type", ""))
        if sig in prev_signatures:
            skipped.append(f)
        else:
            healable.append(f)
    return healable, skipped


def build_heal_context(report: dict, heal_count: int) -> dict | None:
    """실패 테스트의 traceback을 모아 heal_context.json 생성. 실패 없으면 None 반환.

    단일 파이프라인(06_heal.py)과 동일한 플로우:
    1. 실패 수집 + 스크린샷 연결
    2. classify_error로 에러 분류 + failure_groups 구성
    3. 사이트 사전 접근 체크
    4. 반복 실패 감지 (_detect_repeated_failures_parallel)
    5. append_lessons + update_heal_stats
    """
    failures = []
    for t in report.get("tests", []):
        if t.get("outcome") in ("failed", "error"):
            call = t.get("call") or {}
            longrepr = call.get("longrepr", "")
            if isinstance(longrepr, dict):
                longrepr = longrepr.get("reprcrash", {}).get("message", str(longrepr))
            test_name = t.get("nodeid", "").split("::")[-1]
            traceback_str = str(longrepr)
            failures.append({
                "test_id": t.get("nodeid", ""),
                "test_name": test_name,
                "file": t.get("nodeid", "").split("::")[0],
                "traceback": traceback_str,
                "error_type": classify_error(traceback_str),
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
                    entry = pages_data[group]
                    urls[group] = entry.get("url") if isinstance(entry, dict) else entry
        except Exception:
            pass

    # 사이트 접근 가능성 사전 체크
    if urls:
        site_err = _check_urls_accessible(urls)
        if site_err:
            print(f"\n[99] 사이트 접근 불가: {site_err['url']} ({site_err['error']})")
            print("     사이트가 다운되었거나 네트워크 문제입니다. 힐링을 건너뜁니다.")
            ctx = {
                "heal_count": heal_count,
                "error": site_err["error"],
                "url": site_err["url"],
                "analyzed_at": datetime.now().isoformat(),
            }
            write_state(HEAL_CONTEXT_STATE, ctx)
            return None  # 힐링 불가 → 호출부에서 heal_failed 처리

    # 에러 타입별 그룹핑
    failure_groups = defaultdict(list)
    for f in failures:
        failure_groups[f["error_type"]].append(f["test_name"])

    # 반복 실패 감지
    prev_ctx = read_state(HEAL_CONTEXT_STATE)
    healable, skipped = _detect_repeated_failures_parallel(failures, prev_ctx)

    if skipped:
        skipped_names = [f["test_name"] for f in skipped]
        print(f"\n[99] 동일 오류 2회 연속 반복 → {len(skipped)}건 스킵:")
        for name in skipped_names:
            print(f"     - {name}")
        for s in skipped:
            slog("heal_skip_repeated", test_name=s["test_name"],
                 error_type=s.get("error_type", ""), pipeline="parallel")

    # 모든 실패가 반복 → 힐링 중단
    if not healable and skipped:
        print("[99] 모든 실패가 반복 패턴 — 수동 수정이 필요합니다.")
        ctx = {
            "heal_count": heal_count,
            "skipped_repeated": [f["test_name"] for f in skipped],
            "error": "모든 실패가 동일 오류 2회 반복. 수동 수정 필요.",
            "analyzed_at": datetime.now().isoformat(),
        }
        write_state(HEAL_CONTEXT_STATE, ctx)
        append_lessons(failures)
        update_heal_stats(failures)
        return None

    # 최신 lessons_learned 스냅샷 (subagent 간 학습 공유)
    lessons_snapshot = ""
    for lpath in [LESSONS_PATH, LESSONS_AUTO_PATH]:
        if lpath.exists():
            try:
                lessons_snapshot += lpath.read_text(encoding="utf-8") + "\n"
            except Exception:
                pass

    ctx = {
        "heal_count": heal_count,
        "failure_count": len(healable),
        "failures": healable,
        "failure_groups": dict(failure_groups),
        "skipped_repeated": [f["test_name"] for f in skipped],
        "urls": urls,
        "lessons_snapshot": lessons_snapshot[-3000:] if lessons_snapshot else "",
        "analyzed_at": datetime.now().isoformat(),
    }
    write_state(HEAL_CONTEXT_STATE, ctx)
    print(f"\n[99] heal_context 저장됨: {HEAL_CONTEXT_STATE}  "
          f"(힐링 대상 {len(healable)}건"
          + (f", 반복 스킵 {len(skipped)}건" if skipped else "") + ")")

    # 실수 패턴 자동 기록 + heal_stats 빈도 업데이트
    append_lessons(healable + skipped)
    update_heal_stats(healable + skipped)

    return ctx


def _try_auto_heal() -> bool:
    """06_auto_heal.py를 subprocess로 호출하여 deterministic 패치 시도.

    Returns:
        True: auto_heal이 일부/전부 패치 성공 (재실행 필요)
        False: 자동 패치 가능한 패턴 없음 (Agent 힐링 필요)
    """
    auto_heal_script = PROJECT_ROOT / "scripts" / "06_auto_heal.py"
    if not auto_heal_script.exists():
        return False
    try:
        result = subprocess.run(
            [PYTHON_EXE, str(auto_heal_script)],
            cwd=str(PROJECT_ROOT),
            capture_output=True, text=True,
            timeout=120,
        )
        # 출력 표시
        if result.stdout.strip():
            for line in result.stdout.strip().splitlines():
                print(f"  {line}")
        # 종료코드 0 = 모든 실패 자동 수정 완료
        return result.returncode == 0
    except (subprocess.TimeoutExpired, Exception) as e:
        print(f"  [auto_heal] 실행 실패 (무시): {e}")
        return False


def print_heal_instructions(heal_context: dict, pipeline: str = "parallel") -> None:
    """배치 분할 병렬 힐링 지시를 출력."""
    failures = heal_context.get("failures", [])
    urls = heal_context.get("urls", {})
    # URL 하나로 통합 (여러 그룹이면 첫 번째)
    url = next(iter(urls.values()), "") if urls else ""

    batches = build_heal_batches(failures)
    print_heal_batches(batches, url=url, pipeline=pipeline)


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

    quick_mode = args.quick
    slog("step_start", step="99_merge", scope=scope_label,
         file_count=len(existing), quick=quick_mode)
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
                # auto_heal 시도 (deterministic 패치)
                auto_heal_applied = _try_auto_heal()
                if auto_heal_applied:
                    print("[99] auto_heal 성공 — Agent 힐링 불필요할 수 있습니다.")
                    print("     python parallel/99_merge.py 를 다시 실행하여 확인하세요.")
                else:
                    pl = "quick" if quick_mode else "parallel"
                print_heal_instructions(heal_ctx, pipeline=pl)
            else:
                # build_heal_context가 None 반환 (사이트 불가 또는 전체 반복)
                HEAL_CONTEXT_STATE.unlink(missing_ok=True)
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
    slog("step_end", step="99_merge", passed=passed, failed=failed,
         total=total, pass_rate=pass_rate, heal_count=heal_count,
         duration_sec=_duration)


if __name__ == "__main__":
    main()
