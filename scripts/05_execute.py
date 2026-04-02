"""
Step 5 — 테스트 실행
LLM 없음. pytest 실행 후 결과를 state/pipeline.json에 저장.
커스텀 다크 테마 HTML 리포트 생성 (병렬 파이프라인 리포트와 동일한 형식).
"""
import ast
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from datetime import datetime
from _python import PYTHON_EXE
from _paths import PIPELINE_STATE, PROJECT_ROOT

TESTCASES_DIR = PROJECT_ROOT / "testcases"
SCREENSHOTS_DIR = PROJECT_ROOT / "tests" / "screenshots"


# ── 케이스 메타데이터 로드 ───────────────────────────────────────


def _load_cases_for_group(group_name: str) -> list:
    """testcases/{group_name}/ 에서 케이스 메타데이터 로드."""
    sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
    try:
        from parse_cases import load_cases as _load_cases
    except ImportError:
        return []
    group_dir = TESTCASES_DIR / group_name
    if group_dir.is_dir():
        return _load_cases(str(group_dir))
    return []


# ── HTML 리포트 헬퍼 ────────────────────────────────────────────


_STEP_NUM_RE = re.compile(r"^\s*\d+[\.\)]\s*")
_BULLET_RE   = re.compile(r"^\s*[-*]\s*")


def _strip_prefix(text: str) -> str:
    """'1. ', '2) ', '- ', '* ' 같은 앞 접두사 제거."""
    t = _STEP_NUM_RE.sub("", text)
    t = _BULLET_RE.sub("", t)
    return t.strip()


def case_row(case: dict, uid: str, is_passed: bool) -> str:
    title = case.get("title", "untitled")
    precondition = case.get("precondition", "")
    steps = case.get("steps", [])
    expected = case.get("expected", "")
    status_cls = "pass" if is_passed else "fail"
    badge_txt = "PASS" if is_passed else "FAIL"

    clean_steps = [_strip_prefix(s) for s in steps if s.strip()]
    steps_html = "".join(f"<li>{s}</li>" for s in clean_steps) if clean_steps else "<li>-</li>"

    pre_lines = [_strip_prefix(l) for l in precondition.splitlines() if l.strip()]
    pre_content = "<br>".join(pre_lines)
    pre_html = (
        f'<div class="detail-row">'
        f'<span class="detail-label">Precondition</span>'
        f'<span class="detail-val">{pre_content}</span>'
        f'</div>'
        if pre_content else ""
    )

    exp_raw = expected.replace("\\n", "\n")
    exp_lines = [_strip_prefix(l) for l in exp_raw.splitlines() if l.strip()]
    exp_content = "<br>".join(exp_lines)

    return f"""<div class="case-item" onclick="toggle('{uid}')">
  <div class="case-header">
    <span class="case-dot {status_cls}"></span>
    <span class="case-title">{title}</span>
    <div class="case-right">
      <span class="case-status-txt {status_cls}">{badge_txt}</span>
      <span class="chevron" id="chv_{uid}">&#8250;</span>
    </div>
  </div>
  <div class="case-detail" id="detail_{uid}">
    {pre_html}
    <div class="detail-row">
      <span class="detail-label">Steps</span>
      <span class="detail-val"><ol class="steps-list">{steps_html}</ol></span>
    </div>
    <div class="detail-row">
      <span class="detail-label">Expected</span>
      <span class="detail-val">{exp_content}</span>
    </div>
  </div>
</div>"""


def build_report_html(test_results: dict, pytest_summary: dict,
                      created_at: str, group_name: str,
                      test_cases: list) -> str:
    """단일 파이프라인용 커스텀 HTML 리포트 생성."""
    pass_total = pytest_summary.get("passed", 0)
    fail_total = pytest_summary.get("failed", 0) + pytest_summary.get("error", 0)
    total = pass_total + fail_total
    pass_rate = round(pass_total / total * 100, 1) if total else 0
    all_pass = fail_total == 0
    overall_cls = "pass" if all_pass else "fail"
    overall_txt = "ALL PASS" if all_pass else f"{fail_total} FAILED"

    # 사이드바 nav: 그룹 1개
    display_label = group_name.replace("_", " ").upper()
    nav_items = f'<li class="nav-item" onclick="scrollTo(\'{group_name}\')">{display_label}</li>\n'

    # 케이스별 결과 매칭
    rows_html = ""
    if test_cases:
        # 케이스를 test_results와 매칭 (파일 stem으로)
        group_passed = all(test_results.values()) if test_results else False

        for case_idx, case in enumerate(test_cases):
            uid = f"{group_name}_{case_idx}"
            # 케이스별 매칭: 개별 테스트 결과를 케이스 인덱스로 추정
            test_items = list(test_results.items())
            if case_idx < len(test_items):
                is_passed = test_items[case_idx][1]
            else:
                is_passed = group_passed
            rows_html += case_row(case, uid, is_passed)
    else:
        # 케이스 메타데이터 없으면 파일 단위로 표시
        for idx, (nodeid, is_passed) in enumerate(test_results.items()):
            uid = f"{group_name}_{idx}"
            simple_case = {
                "title": nodeid.split("::")[-1].replace("_", " ").title() if "::" in nodeid else nodeid,
                "precondition": "",
                "steps": [],
                "expected": "",
            }
            rows_html += case_row(simple_case, uid, is_passed)

    if not rows_html:
        rows_html = '<p class="empty-msg">케이스 정보 없음</p>'

    # 그룹 통계
    g_pass_cnt = sum(1 for v in test_results.values() if v)
    g_total_cnt = len(test_results)
    g_passed = all_pass
    status_cls = "pass" if g_passed else ("fail" if test_results else "warn")
    status_txt = "PASS" if g_passed else ("FAIL" if test_results else "N/A")

    group_section = f"""
<section class="group-card" id="group_{group_name}">
  <div class="group-header {status_cls}">
    <div class="group-title-wrap">
      <span class="group-dot {status_cls}"></span>
      <span class="group-title">{display_label}</span>
      <span class="group-sub">{g_pass_cnt} / {g_total_cnt} passed</span>
    </div>
    <div class="group-right">
      <span class="badge {status_cls}">{status_txt}</span>
    </div>
  </div>
  <div class="case-list">{rows_html}</div>
</section>"""

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>QA Report</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
  :root {{
    --bg:#0f1117;--surface:#1a1d27;--surface2:#21242f;--border:#2e3140;
    --text:#e8eaf0;--text2:#8b8fa8;--text3:#555870;
    --pass:#22c55e;--pass-bg:rgba(34,197,94,.1);
    --fail:#ef4444;--fail-bg:rgba(239,68,68,.1);
    --warn:#f59e0b;--warn-bg:rgba(245,158,11,.1);
    --accent:#6366f1;--radius:12px;--radius-sm:8px;
  }}
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{font-family:'Inter',-apple-system,sans-serif;background:var(--bg);color:var(--text);min-height:100vh}}
  .layout{{display:grid;grid-template-columns:220px 1fr;min-height:100vh}}
  .sidebar{{background:var(--surface);border-right:1px solid var(--border);padding:28px 0;position:sticky;top:0;height:100vh;overflow-y:auto}}
  .sidebar-logo{{padding:0 20px 24px;border-bottom:1px solid var(--border);margin-bottom:16px}}
  .logo-text{{font-size:15px;font-weight:700}}
  .logo-sub{{font-size:11px;color:var(--text3);margin-top:3px}}
  .nav-section{{padding:0 12px}}
  .nav-label{{font-size:10px;font-weight:600;color:var(--text3);text-transform:uppercase;letter-spacing:1px;padding:0 8px;margin-bottom:6px}}
  .nav-item{{font-size:13px;color:var(--text2);padding:8px 10px;border-radius:var(--radius-sm);cursor:pointer;transition:all .15s;list-style:none;font-weight:500}}
  .nav-item:hover{{background:var(--surface2);color:var(--text)}}
  .main{{padding:36px 40px;max-width:900px}}
  .topbar{{display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:32px}}
  .topbar h1{{font-size:24px;font-weight:700;letter-spacing:-.5px}}
  .meta{{font-size:12px;color:var(--text3);margin-top:5px}}
  .overall-badge{{display:flex;align-items:center;gap:8px;padding:10px 18px;border-radius:var(--radius);font-size:13px;font-weight:700;letter-spacing:.3px}}
  .overall-badge.pass{{background:var(--pass-bg);color:var(--pass);border:1px solid rgba(34,197,94,.2)}}
  .overall-badge.fail{{background:var(--fail-bg);color:var(--fail);border:1px solid rgba(239,68,68,.2)}}
  .stats{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:32px}}
  .stat-card{{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:20px 22px;transition:border-color .2s}}
  .stat-card:hover{{border-color:var(--accent)}}
  .stat-num{{font-size:32px;font-weight:700;letter-spacing:-1px;line-height:1;margin-bottom:6px}}
  .stat-lbl{{font-size:12px;color:var(--text3);font-weight:500;text-transform:uppercase;letter-spacing:.5px}}
  .group-card{{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);margin-bottom:16px;overflow:hidden;transition:border-color .2s}}
  .group-card:hover{{border-color:#3a3d50}}
  .group-header{{display:flex;align-items:center;justify-content:space-between;padding:16px 20px;border-bottom:1px solid var(--border)}}
  .group-header.pass{{border-left:3px solid var(--pass)}}
  .group-header.fail{{border-left:3px solid var(--fail)}}
  .group-header.warn{{border-left:3px solid var(--warn)}}
  .group-title-wrap{{display:flex;align-items:center;gap:10px}}
  .group-dot{{width:8px;height:8px;border-radius:50%;flex-shrink:0}}
  .group-dot.pass{{background:var(--pass);box-shadow:0 0 6px var(--pass)}}
  .group-dot.fail{{background:var(--fail);box-shadow:0 0 6px var(--fail)}}
  .group-dot.warn{{background:var(--warn);box-shadow:0 0 6px var(--warn)}}
  .group-title{{font-size:14px;font-weight:700;letter-spacing:.5px}}
  .group-sub{{font-size:12px;color:var(--text3)}}
  .group-right{{display:flex;align-items:center;gap:8px}}
  .badge{{font-size:11px;font-weight:700;padding:3px 10px;border-radius:20px;letter-spacing:.5px}}
  .badge.pass{{background:var(--pass-bg);color:var(--pass);border:1px solid rgba(34,197,94,.25)}}
  .badge.fail{{background:var(--fail-bg);color:var(--fail);border:1px solid rgba(239,68,68,.25)}}
  .badge.warn{{background:var(--warn-bg);color:var(--warn);border:1px solid rgba(245,158,11,.25)}}
  .case-list{{padding:8px 0}}
  .case-item{{border-bottom:1px solid var(--border);cursor:pointer;transition:background .1s}}
  .case-item:last-child{{border-bottom:none}}
  .case-item:hover{{background:var(--surface2)}}
  .case-header{{display:flex;align-items:center;gap:12px;padding:12px 20px}}
  .case-dot{{width:6px;height:6px;border-radius:50%;flex-shrink:0}}
  .case-dot.pass{{background:var(--pass)}}.case-dot.fail{{background:var(--fail)}}
  .case-title{{flex:1;font-size:13px;font-weight:500;color:var(--text);line-height:1.4}}
  .case-right{{display:flex;align-items:center;gap:10px;flex-shrink:0}}
  .case-status-txt{{font-size:11px;font-weight:700;letter-spacing:.5px}}
  .case-status-txt.pass{{color:var(--pass)}}
  .case-status-txt.fail{{color:var(--fail)}}
  .chevron{{color:var(--text3);font-size:18px;transition:transform .2s;display:inline-block}}
  .chevron.open{{transform:rotate(90deg)}}
  .case-detail{{display:none;padding:0 20px 16px 38px;animation:fadeIn .15s ease}}
  @keyframes fadeIn{{from{{opacity:0;transform:translateY(-4px)}}to{{opacity:1;transform:none}}}}
  .detail-row{{display:flex;gap:16px;margin-top:10px;font-size:12px;line-height:1.6}}
  .detail-label{{min-width:90px;font-weight:600;color:var(--text3);text-transform:uppercase;font-size:10px;letter-spacing:.5px;padding-top:2px;flex-shrink:0}}
  .detail-val{{color:var(--text2)}}
  .steps-list{{padding-left:16px;margin:0}}
  .steps-list li{{margin:3px 0}}
  .empty-msg{{padding:16px 20px;font-size:13px;color:var(--text3)}}
</style>
<script>
function toggle(uid){{
  var d=document.getElementById('detail_'+uid);
  var c=document.getElementById('chv_'+uid);
  if(d.style.display==='none'||!d.style.display){{d.style.display='block';c.classList.add('open');}}
  else{{d.style.display='none';c.classList.remove('open');}}
}}
function scrollTo(label){{
  var el=document.getElementById('group_'+label);
  if(el)el.scrollIntoView({{behavior:'smooth',block:'start'}});
}}
</script>
</head>
<body>
<div class="layout">
  <aside class="sidebar">
    <div class="sidebar-logo">
      <div class="logo-text">QA Native</div>
      <div class="logo-sub">Test Report</div>
    </div>
    <nav class="nav-section">
      <div class="nav-label">Groups</div>
      <ul style="list-style:none;">{nav_items}</ul>
    </nav>
  </aside>
  <div class="main">
    <div class="topbar">
      <div>
        <h1>Test Results</h1>
        <div class="meta">{created_at} &middot; 1 group &middot; {total} cases</div>
      </div>
      <div class="overall-badge {overall_cls}">{overall_txt}</div>
    </div>
    <div class="stats">
      <div class="stat-card"><div class="stat-num" style="color:var(--text);">{total}</div><div class="stat-lbl">Total</div></div>
      <div class="stat-card"><div class="stat-num" style="color:var(--pass);">{pass_total}</div><div class="stat-lbl">Passed</div></div>
      <div class="stat-card"><div class="stat-num" style="color:var(--fail);">{fail_total}</div><div class="stat-lbl">Failed</div></div>
      <div class="stat-card"><div class="stat-num" style="color:{'var(--pass)' if all_pass else 'var(--fail)'};">{pass_rate}%</div><div class="stat-lbl">Pass Rate</div></div>
    </div>
    {group_section}
  </div>
</div>
</body>
</html>"""


# ── pytest 결과 파싱 ────────────────────────────────────────────


def parse_results(report: dict) -> dict:
    """JSON 리포트 → {nodeid: passed} 매핑."""
    results = {}
    for t in report.get("tests", []):
        nodeid = t.get("nodeid", "")
        results[nodeid] = t.get("outcome") == "passed"
    return results


# ── 테스트 함수 수 계산 ─────────────────────────────────────────


def count_test_functions(file_path: str) -> tuple[int, bool]:
    """테스트 함수 수와 의존성 여부 반환."""
    p = Path(file_path)
    try:
        if p.is_dir():
            total = 0
            for f in sorted(p.glob("*.py")):
                if f.name in ("__init__.py", "conftest.py"):
                    continue
                tree = ast.parse(f.read_text(encoding="utf-8"))
                total += sum(1 for n in tree.body
                             if isinstance(n, ast.FunctionDef) and n.name.startswith("test_"))
            # 디렉토리 내 파일별 1함수이므로 의존성 없음
            return total, False
        tree = ast.parse(p.read_text(encoding="utf-8"))
        funcs = [n for n in tree.body
                 if isinstance(n, ast.FunctionDef) and n.name.startswith("test_")]
        return len(funcs), len(funcs) > 1
    except Exception:
        return 1, False


# ── 그룹명 추출 ────────────────────────────────────────────────


def _extract_group_name(state: dict) -> str:
    """pipeline.json에서 그룹명(테스트케이스 폴더명) 추출."""
    # group_dir 필드 직접 사용 (신규)
    if state.get("group_dir"):
        return state["group_dir"]

    # test_cases[0]의 파일 경로 또는 url에서 추출 시도
    cases_path = state.get("cases_path", "")
    if cases_path:
        p = Path(cases_path)
        if p.is_dir():
            return p.name
        return p.parent.name

    # generated_file_path에서 상위 폴더명 추출 시도
    file_path = state.get("generated_file_path", "")
    if file_path:
        p = Path(file_path)
        # tests/generated/{group}/test_xxx.py 또는 tests/generated/test_xxx.py
        parts = p.parts
        if "generated" in parts:
            idx = list(parts).index("generated")
            if idx + 2 < len(parts):  # generated/{group}/file.py
                return parts[idx + 1]

    # URL에서 도메인/패스 마지막 세그먼트 추출
    url = state.get("url", "")
    if url:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        path_parts = [p for p in parsed.path.split("/") if p]
        if path_parts:
            return path_parts[-1]
        return parsed.netloc.split(".")[0] if parsed.netloc else "test"

    return "test"


# ── 메인 ────────────────────────────────────────────────────────


def main():
    # --no-report 플래그: 힐링 중간 실행 시 리포트 생성 건너뛰기
    no_report = "--no-report" in sys.argv

    state_path = PIPELINE_STATE
    if not state_path.exists():
        print("[오류] state/pipeline.json 없음.")
        sys.exit(1)

    state = json.loads(state_path.read_text(encoding="utf-8"))

    if state.get("approval_status") != "approved":
        print("[오류] 미승인 상태. 04_approve.py를 먼저 실행하세요.")
        sys.exit(1)

    file_path = state.get("generated_file_path", "tests/generated/test_generated.py")
    if not Path(file_path).exists():
        print(f"[오류] 테스트 파일 없음: {file_path}")
        sys.exit(1)

    # 매 실행 전 스크린샷 초기화 (최종 실패 스크린샷만 남기기)
    if SCREENSHOTS_DIR.exists():
        shutil.rmtree(SCREENSHOTS_DIR, ignore_errors=True)

    # 리포트 경로
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report_dir = PROJECT_ROOT / "tests" / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / f"report_{ts}.html"

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

    # JSON 리포트 임시 경로
    json_report_path = Path(tempfile.gettempdir()) / f"qa_single_report_{ts}.json"

    result = subprocess.run(
        [
            PYTHON_EXE, "-m", "pytest", file_path,
            "--json-report",
            f"--json-report-file={json_report_path}",
            "-v",
            "--tb=short",
        ] + parallel_opts,
        capture_output=False,   # 실시간 출력
        text=True,
    )

    # JSON 리포트 파싱
    report = {}
    if json_report_path.exists():
        try:
            report = json.loads(json_report_path.read_text(encoding="utf-8"))
        except Exception:
            pass
        json_report_path.unlink(missing_ok=True)

    pytest_summary = report.get("summary", {})
    test_results = parse_results(report)

    # pytest 종료코드로 보완
    passed_count = pytest_summary.get("passed", 0)
    failed_count = pytest_summary.get("failed", 0) + pytest_summary.get("error", 0)

    # JSON 리포트가 비어있으면 종료코드로 판단
    if not test_results:
        passed_count = 0 if result.returncode != 0 else 1
        failed_count = 1 if result.returncode != 0 else 0

    # 그룹명 추출
    group_name = _extract_group_name(state)

    # 케이스 메타데이터 로드
    test_cases = state.get("test_cases", [])
    if not test_cases:
        test_cases = _load_cases_for_group(group_name)

    # 커스텀 HTML 리포트 생성 (힐링 중간 실행 시 건너뛰기)
    if not no_report:
        html_content = build_report_html(
            test_results=test_results,
            pytest_summary=pytest_summary,
            created_at=now,
            group_name=group_name,
            test_cases=test_cases,
        )
        report_path.write_text(html_content, encoding="utf-8")

    # 결과 집계
    total = passed_count + failed_count
    pass_rate = round(passed_count / total * 100, 1) if total else 0
    summary = f"{passed_count} passed, {failed_count} failed" if total else "결과 없음"

    # 그룹별 결과 (병렬 파이프라인과 동일 구조)
    group_results = {}
    if test_results:
        gr = {"passed": 0, "failed": 0, "tests": []}
        for nodeid, is_passed in test_results.items():
            if is_passed:
                gr["passed"] += 1
            else:
                gr["failed"] += 1
            gr["tests"].append({
                "nodeid": nodeid,
                "name": nodeid.split("::")[-1] if "::" in nodeid else nodeid,
                "passed": is_passed,
            })
        group_results[group_name] = gr

    execution_result = {
        "passed":      passed_count,
        "failed":      failed_count,
        "total":       total,
        "pass_rate":   pass_rate,
        "exit_code":   result.returncode,
        "summary":     summary,
        "report_path": str(report_path) if not no_report else "",
        "report_name": report_path.name if not no_report else "",
        "group_results": group_results,
        "executed_at": now,
        "heal_count":  state.get("heal_count", 0),
    }

    state["execution_result"] = execution_result
    state["step"] = "done"
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

    print()
    print("=" * 55)
    all_pass = failed_count == 0
    status = "성공" if all_pass else "실패"
    print(f"  테스트 {status}: {summary}")
    if not no_report:
        print(f"  HTML 리포트: {report_path}")
    else:
        print("  (힐링 중 — 리포트 생성 건너뜀)")
    print("=" * 55)


if __name__ == "__main__":
    main()
