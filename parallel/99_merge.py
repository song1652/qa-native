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
import re
import shutil
import subprocess
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict

PROJECT_ROOT = Path(__file__).parent.parent
GENERATED_DIR = PROJECT_ROOT / "tests" / "generated"
TESTCASES_DIR = PROJECT_ROOT / "testcases"
HEAL_CONTEXT_PATH = PROJECT_ROOT / "state" / "heal_context.json"
PARALLEL_STATE_PATH = PROJECT_ROOT / "state" / "parallel.json"
LESSONS_PATH = PROJECT_ROOT / "agents" / "lessons_learned.md"
SCREENSHOTS_DIR = PROJECT_ROOT / "tests" / "screenshots"
MAX_HEAL = 3

sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
from _python import PYTHON_EXE
try:
    from parse_cases import load_cases as _load_cases
except ImportError:
    _load_cases = None


# ── 상태 업데이트 헬퍼 ──────────────────────────────────────────


def _update_parallel_status(status: str, extra: dict | None = None) -> None:
    """state/parallel.json의 status 필드를 업데이트 (기존 데이터 보존)."""
    state = {}
    if PARALLEL_STATE_PATH.exists():
        try:
            state = json.loads(
                PARALLEL_STATE_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    state["status"] = status
    if extra:
        state.update(extra)
    PARALLEL_STATE_PATH.write_text(
        json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


# ── lessons_learned 자동 기록 ────────────────────────────────────


def classify_error(traceback: str) -> str:
    """traceback에서 오류 유형 분류."""
    tb = traceback.lower()
    if any(k in tb for k in ["strict mode violation", "element not found",
                              "locator", "no element", "getby"]):
        return "Locator"
    if any(k in tb for k in ["expected", "to contain", "assertionerror",
                              "to have text", "to have url"]):
        return "Assertion"
    if "timeout" in tb:
        return "Timeout"
    if any(k in tb for k in ["url", "goto", "navigation"]):
        return "URL"
    return "기타"


def extract_key_lines(traceback: str) -> list[str]:
    """트레이스백에서 핵심 오류 라인 최대 3개 추출."""
    lines = traceback.splitlines()
    key = [l.strip() for l in lines
           if any(k in l for k in ["Error", "Expected", "assert",
                                    "expect", "Locator"])]
    return key[:3]


def append_lessons(failures: list[dict]) -> None:
    """실패 케이스를 lessons_learned.md에 자동 추가 (병렬 파이프라인용)."""
    if not failures or not LESSONS_PATH.exists():
        return

    today = datetime.now().strftime("%Y-%m-%d")
    new_entries: dict[str, list[str]] = {}

    for f in failures:
        error_type = classify_error(f["traceback"])
        key_lines = extract_key_lines(f["traceback"])
        error_summary = key_lines[0] if key_lines else "(traceback 없음)"
        file_name = f.get("file", "unknown")

        fix_hint = ""
        if error_type == "Locator":
            fix_hint = "→ dom_info 셀렉터 재확인, #id 우선 사용"
        elif error_type == "Assertion":
            fix_hint = "→ 실제 페이지 텍스트/상태로 기댓값 수정"
        elif error_type == "Timeout":
            fix_hint = "→ expect(..., timeout=10000) 또는 wait_for_selector 추가"
        elif error_type == "URL":
            fix_hint = "→ BASE_URL 또는 goto 인자 재확인"

        entry = (
            f"\n### [힐링 대기] {today} — {file_name}\n"
            f"- **문제**: `{error_summary}`\n"
            f"- **수정**: (힐링 후 Claude Code가 자동 기입)\n"
            f"- **재발 방지**: {fix_hint}\n"
        )
        new_entries.setdefault(error_type, []).append(entry)

    content = LESSONS_PATH.read_text(encoding="utf-8")

    for section, entries in new_entries.items():
        section_header = (f"## {section} 오류"
                          if section != "기타" else "## 기타")
        insert_text = "\n" + "".join(entries)
        pattern = rf"({re.escape(section_header)}[^\n]*\n(?:<!--[^>]*-->\n)?)"
        if re.search(pattern, content):
            content = re.sub(
                pattern, r"\1" + insert_text, content, count=1)
        else:
            content += f"\n{section_header}\n{insert_text}"

    LESSONS_PATH.write_text(content, encoding="utf-8")
    print(f"[99] lessons_learned.md 업데이트: "
          f"{sum(len(v) for v in new_entries.values())}건 추가")


# ── 스크린샷 검색 ────────────────────────────────────────────────


def find_screenshot_for_test(test_name: str) -> dict | None:
    """tests/screenshots/ 에서 테스트명에 매칭되는 스크린샷과 메타데이터를 찾는다."""
    if not SCREENSHOTS_DIR.exists():
        return None
    # 그룹 접두사 패턴 우선 검색 (group__test_name.png)
    candidates = list(SCREENSHOTS_DIR.glob(f"*__{test_name}.png"))
    if not candidates:
        # 이전 형식 fallback (test_name.png)
        candidates = list(SCREENSHOTS_DIR.glob(f"{test_name}.png"))
    if not candidates:
        return None
    shot_path = candidates[0]
    result = {"path": str(shot_path)}
    meta_path = shot_path.with_suffix("").with_suffix(".meta.json")
    if meta_path.exists():
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            result["url"] = meta.get("url")
            result["timestamp"] = meta.get("timestamp")
        except Exception:
            pass
    return result


# ── pytest 실행 ──────────────────────────────────────────────────


def parse_results(report: dict) -> dict:
    """JSON 리포트 → {nodeid: passed} 매핑."""
    results = {}
    for t in report.get("tests", []):
        nodeid = t.get("nodeid", "")
        results[nodeid] = t.get("outcome") == "passed"
    return results


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
    HEAL_CONTEXT_PATH.write_text(json.dumps(ctx, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n[99] heal_context 저장됨: {HEAL_CONTEXT_PATH}  ({len(failures)}건 실패)")

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
    print(f"  heal_context 저장: {HEAL_CONTEXT_PATH}")
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
    # tests/generated/ 디렉토리 스캔으로 그룹 구성 (대상 그룹만 필터)
    groups = _scan_generated_groups()
    if target_groups:
        groups = {k: v for k, v in groups.items() if k in target_groups}

    pass_total = summary.get("passed", 0)
    fail_total = summary.get("failed", 0) + summary.get("error", 0)
    total = pass_total + fail_total
    pass_rate = round(pass_total / total * 100, 1) if total else 0
    all_pass = fail_total == 0
    overall_cls = "pass" if all_pass else "fail"
    overall_txt = "ALL PASS" if all_pass else f"{fail_total} FAILED"

    nav_items = ""
    for label in groups:
        nav_items += f'<li class="nav-item" onclick="scrollTo(\'{label}\')">{label.replace("_"," ").upper()}</li>\n'

    group_sections = ""
    for label, files in groups.items():
        # 이 그룹에 해당하는 테스트 결과 추출
        group_tests = {
            k: v for k, v in test_results.items()
            if f"/{label}/" in k or f"\\{label}\\" in k
        }
        g_passed = all(group_tests.values()) if group_tests else False
        g_pass_cnt = sum(1 for v in group_tests.values() if v)
        g_total_cnt = len(group_tests)

        status_cls = "pass" if g_passed else ("fail" if group_tests else "warn")
        status_txt = "PASS" if g_passed else ("FAIL" if group_tests else "N/A")

        # 케이스 메타데이터 로드 (testcases/{group}/)
        cases = _load_cases_for_group(label)
        rows_html = ""

        if cases:
            for case_idx, case in enumerate(cases):
                uid = f"{label}_{case_idx}"
                # 케이스별 결과 매칭: 파일별로 결과 확인
                case_pass = all(group_tests.values()) if group_tests else False
                rows_html += case_row(case, uid, case_pass)
        else:
            # 케이스 메타데이터 없으면 파일 단위로 표시
            for file_idx, f in enumerate(files):
                uid = f"{label}_{file_idx}"
                nodeid_match = next(
                    (k for k in test_results
                     if f.stem in k),
                    None
                )
                is_passed = test_results.get(nodeid_match, False) if nodeid_match else False
                simple_case = {
                    "title": f.stem.replace("_", " ").title(),
                    "precondition": "",
                    "steps": [],
                    "expected": "",
                }
                rows_html += case_row(simple_case, uid, is_passed)

        if not rows_html:
            rows_html = '<p class="empty-msg">케이스 정보 없음</p>'

        display_label = label.replace("_", " ").upper()
        group_sections += f"""
<section class="group-card" id="group_{label}">
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
      <div class="logo-sub">Parallel Test Report</div>
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
        <div class="meta">{created_at} &middot; {len(groups)} groups &middot; {total} cases</div>
      </div>
      <div class="overall-badge {overall_cls}">{overall_txt}</div>
    </div>
    <div class="stats">
      <div class="stat-card"><div class="stat-num" style="color:var(--text);">{total}</div><div class="stat-lbl">Total</div></div>
      <div class="stat-card"><div class="stat-num" style="color:var(--pass);">{pass_total}</div><div class="stat-lbl">Passed</div></div>
      <div class="stat-card"><div class="stat-num" style="color:var(--fail);">{fail_total}</div><div class="stat-lbl">Failed</div></div>
      <div class="stat-card"><div class="stat-num" style="color:{'var(--pass)' if all_pass else 'var(--fail)'};">{pass_rate}%</div><div class="stat-lbl">Pass Rate</div></div>
    </div>
    {group_sections}
  </div>
</div>
</body>
</html>"""


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
    args = parser.parse_args()
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

    n_workers = min(len(existing), 4)

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
    if HEAL_CONTEXT_PATH.exists():
        try:
            prev = json.loads(HEAL_CONTEXT_PATH.read_text(encoding="utf-8"))
            heal_count = prev.get("heal_count", 0)
            heal_analyzed_at = prev.get("analyzed_at")
        except Exception:
            pass

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

    # 빠른 실행 모드에서는 state/quick.json 사용, parallel_state 미변경
    quick_mode = args.quick or bool(args.group)
    QUICK_STATE_PATH = PROJECT_ROOT / "state" / "quick.json"
    state_path = QUICK_STATE_PATH if quick_mode else PARALLEL_STATE_PATH

    if not quick_mode:
        _update_parallel_status("testing")

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_report_path = Path(tempfile.gettempdir()) / f"qa_report_{ts}.json"

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
    )
    pytest_exit_code = proc.returncode
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
        if heal_count >= MAX_HEAL:
            print(f"\n[99] 최대 힐링 횟수({MAX_HEAL}회) 초과 — 수동 수정이 필요합니다.")
            HEAL_CONTEXT_PATH.unlink(missing_ok=True)
        else:
            heal_count += 1
            heal_ctx = build_heal_context(report, heal_count)
            if heal_ctx:
                print_heal_instructions(heal_ctx)
    else:
        HEAL_CONTEXT_PATH.unlink(missing_ok=True)

    # 4. HTML 리포트 (힐링 완료 후에만 생성: 전체 통과 또는 최대 힐링 초과)
    is_final_run = (not has_issues) or heal_count >= MAX_HEAL
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

    run_state = {}
    if state_path.exists():
        try:
            run_state = json.loads(state_path.read_text(encoding="utf-8"))
        except Exception:
            pass

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
    elif heal_count >= MAX_HEAL:
        run_state["status"] = "heal_failed"
    else:
        run_state["status"] = "heal_needed"
    state_path.write_text(
        json.dumps(run_state, ensure_ascii=False, indent=2), encoding="utf-8"
    )

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
