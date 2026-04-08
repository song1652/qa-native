"""
병렬 파이프라인 Step 99 - 실행 + 결과 병합 + 통합 리포트

1. workers/ 에서 생성된 테스트 코드를 tests/generated/{group}/ 로 수집
2. tests/generated/ 에서 pytest 일괄 실행 (JSON 리포트)
3. 실패 시 heal_context 저장 → Claude Code 힐링 루프 (최대 3회)
4. 그룹별 PASS/FAIL 집계
5. HTML 리포트 생성 (tests/reports/parallel_index_{ts}.html)
6. workers/ 비우기

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
HEAL_CONTEXT_PATH = PROJECT_ROOT / "parallel" / "heal_context.json"
MAX_HEAL = 3

sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
try:
    from parse_cases import load_cases as _load_cases
except ImportError:
    _load_cases = None


def title_to_funcname(title: str) -> str:
    snake = re.sub(r"[^a-zA-Z0-9]+", "_", title.lower()).strip("_")
    return f"test_{snake}"


def cases_file_to_funcname(cases_file: str) -> str:
    """cases_file 경로(tc_NN_xxx.md)에서 테스트 함수명 추출."""
    stem = Path(cases_file).stem  # e.g. tc_01_login_success
    m = re.match(r"tc_\d+_(.*)", stem)
    name = m.group(1) if m else stem
    return f"test_{name}"


# ── 테스트 파일 수집 ─────────────────────────────────────────────


def get_group_label(worker: dict) -> str:
    label = worker.get("group_label")
    if not label:
        cf = Path(worker.get("cases_file", ""))
        if cf.parent.name and cf.parent.name not in ("config", ".", ""):
            label = cf.parent.name
        else:
            parts = cf.stem.split("_")
            label = "_".join(p for p in parts if not p.isdigit() and p not in ("internet",)) or cf.stem
    return label


def collect_tests(batch_state: dict) -> dict:
    """worker별 test_generated.py → tests/generated/{group}/test_{function_name}.py (케이스 1개 = 파일 1개)"""
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)

    collected = {}  # fn_name → out_path
    for w in batch_state["workers"]:
        label = get_group_label(w)
        group_dir = GENERATED_DIR / label
        group_dir.mkdir(exist_ok=True)

        worker_dir = PROJECT_ROOT / w["worker_dir"]
        test_file = worker_dir / "tests" / "generated" / "test_generated.py"
        if not test_file.exists():
            print(f"  [경고] 파일 없음: {test_file}")
            continue

        src = test_file.read_text(encoding="utf-8")
        imports, functions = extract_code(src)

        for fn_src in functions:
            match = re.match(r"def (test_\w+)", fn_src)
            if not match:
                continue
            fn_name = match.group(1)
            out_path = group_dir / f"{fn_name}.py"
            content = "\n".join(imports) + "\n\n\n" + fn_src + "\n"
            out_path.write_text(content, encoding="utf-8")
            collected[fn_name] = out_path
            print(f"  collected: {label}/{fn_name}.py")

    return collected


def extract_code(source: str) -> tuple[list[str], list[str]]:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return [], []
    lines = source.splitlines()
    imports = []
    functions = []
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            line = lines[node.lineno - 1].strip()
            if line not in imports:
                imports.append(line)
        elif isinstance(node, ast.Assign):
            # 모듈 레벨 상수 (BASE_URL 등) 보존
            line = lines[node.lineno - 1].strip()
            if line not in imports:
                imports.append(line)
        elif isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
            fn = "\n".join(lines[node.lineno - 1: node.end_lineno])
            functions.append(fn)
    return imports, functions


# ── pytest 실행 ──────────────────────────────────────────────────


def run_pytest(json_report_path: Path) -> dict:
    """tests/generated/ 전체를 pytest로 실행. JSON 리포트 반환 후 파일 삭제."""
    subprocess.run(
        [
            sys.executable, "-m", "pytest",
            str(GENERATED_DIR),
            f"--json-report",
            f"--json-report-file={json_report_path}",
            "--tb=short",
            "-v",
        ],
        cwd=str(PROJECT_ROOT),
        capture_output=False,
    )
    if json_report_path.exists():
        data = json.loads(json_report_path.read_text(encoding="utf-8"))
        json_report_path.unlink()   # 파싱 후 즉시 삭제
        return data
    return {"tests": [], "summary": {}}


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
            # longrepr이 dict인 경우 처리
            if isinstance(longrepr, dict):
                longrepr = longrepr.get("reprcrash", {}).get("message", str(longrepr))
            failures.append({
                "test_id": t.get("nodeid", ""),
                "test_name": t.get("nodeid", "").split("::")[-1],
                "file": t.get("nodeid", "").split("::")[0],
                "traceback": str(longrepr),
            })
    if not failures:
        return None
    ctx = {
        "heal_count": heal_count,
        "failure_count": len(failures),
        "failures": failures,
        "analyzed_at": datetime.now().isoformat(),
    }
    HEAL_CONTEXT_PATH.write_text(json.dumps(ctx, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n[99] heal_context 저장됨: {HEAL_CONTEXT_PATH}  ({len(failures)}건 실패)")
    return ctx


def print_heal_instructions(heal_context: dict) -> None:
    """Claude Code가 힐링할 수 있도록 컨텍스트를 stdout에 출력."""
    print("\n" + "=" * 60)
    print("  ⚠  테스트 실패 — 힐링 필요")
    print("=" * 60)
    print(f"  heal_count : {heal_context['heal_count']} / {MAX_HEAL}")
    print(f"  failures   : {heal_context['failure_count']}건")
    print()
    for f in heal_context["failures"]:
        print(f"  [{f['test_name']}]")
        # traceback 앞 10줄만 출력
        lines = f["traceback"].splitlines()[:10]
        for line in lines:
            print(f"    {line}")
        print()
    print(f"  heal_context 저장: {HEAL_CONTEXT_PATH}")
    print()
    print("  Claude Code는 위 traceback을 보고 해당 테스트 파일을 패치한 후")
    print("  python parallel/99_merge.py 를 다시 실행하세요.")
    print("=" * 60)


# ── HTML 리포트 ──────────────────────────────────────────────────


def build_html(batch_state: dict, test_results: dict, summary: dict,
               created_at: str, collected: dict) -> str:
    p_color = "var(--pass)"
    f_color = "var(--fail)"

    # group_dir 기준으로 묶기 (같은 사이트/폴더 → 카드 1개)
    # group_dir 없으면 group_label fallback
    groups = defaultdict(list)
    for w in batch_state["workers"]:
        key = w.get("group_dir") or get_group_label(w)
        groups[key].append(w)

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
    for label, workers in groups.items():
        # label(예: login_000) 에 해당하는 테스트 결과 추출
        # 파일 구조: tests/generated/login/login_000.py 또는 tests/generated/login_000/...
        group_tests = {
            k: v for k, v in test_results.items()
            if f"/{label}/" in k or f"\\{label}\\" in k
            or f"/{label}.py" in k or f"\\{label}.py" in k
        }
        g_passed = all(group_tests.values()) if group_tests else False
        g_pass_cnt = sum(1 for v in group_tests.values() if v)
        g_total_cnt = len(group_tests)

        status_cls = "pass" if g_passed else ("fail" if group_tests else "warn")
        status_txt = "PASS" if g_passed else ("FAIL" if group_tests else "N/A")

        # 케이스 rows: state.json → 없으면 cases_file(.md) fallback
        rows_html = ""
        case_idx = 0

        for w in workers:
            # 케이스 목록 로드
            cases = []
            worker_dir = PROJECT_ROOT / w["worker_dir"]
            state_path = worker_dir / "state.json"
            if state_path.exists():
                state = json.loads(state_path.read_text(encoding="utf-8"))
                cases = state.get("test_cases", [])
            elif _load_cases:
                cf = PROJECT_ROOT / w.get("cases_file", "")
                if cf.exists():
                    cases = _load_cases(str(cf))

            # worker의 group_label 파일명으로 테스트 결과 매칭
            w_label = w.get("group_label", label)
            w_pass = next(
                (v for k, v in test_results.items()
                 if f"/{w_label}.py" in k or f"\\{w_label}.py" in k
                 or f"/{w_label}/" in k or f"\\{w_label}\\" in k),
                None
            )
            # 매칭 실패 시 group_tests 전체 결과로 fallback
            if w_pass is None:
                w_pass = all(group_tests.values()) if group_tests else False

            for case in cases:
                uid = f"{label}_{case_idx}"
                rows_html += case_row(case, uid, w_pass)
                case_idx += 1

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

    # 스텝 — 이미 포함된 번호/불릿 접두사 제거 후 <ol> 자동 번호 사용
    clean_steps = [_strip_prefix(s) for s in steps if s.strip()]
    steps_html = "".join(f"<li>{s}</li>" for s in clean_steps) if clean_steps else "<li>-</li>"

    # Precondition — 불릿 접두사 제거 후 한 줄씩
    pre_lines = [_strip_prefix(l) for l in precondition.splitlines() if l.strip()]
    pre_content = "<br>".join(pre_lines)
    pre_html = (
        f'<div class="detail-row">'
        f'<span class="detail-label">Precondition</span>'
        f'<span class="detail-val">{pre_content}</span>'
        f'</div>'
        if pre_content else ""
    )

    # Expected — 불릿 접두사 제거 후 한 줄씩
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
    parser = argparse.ArgumentParser(description="QA 테스트 실행 + 리포트 생성")
    parser.add_argument(
        "--group", "-g",
        nargs="*",
        metavar="FOLDER",
        help="실행할 폴더명 (예: login checkout). 생략 시 전체 실행."
    )
    args = parser.parse_args()

    batch_state_path = PROJECT_ROOT / "parallel" / "batch_state.json"
    batch_state = json.loads(batch_state_path.read_text(encoding="utf-8")) if batch_state_path.exists() else {"workers": []}
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 1. 실행 대상 결정
    if args.group:
        # 지정된 폴더만
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
        # 전체
        existing = [f for f in GENERATED_DIR.rglob("*.py") if f.name != "conftest.py"]
        scope_label = "전체"

    if not existing:
        print("[오류] 실행할 테스트 파일 없음.")
        # 사용 가능한 폴더 안내
        available = [d.name for d in GENERATED_DIR.iterdir() if d.is_dir()]
        if available:
            print(f"  사용 가능한 폴더: {', '.join(available)}")
            print(f"  예시: python parallel/99_merge.py --group {available[0]}")
        return

    collected = {f.stem: f for f in existing}
    n_workers = min(len(existing), 4)  # 최대 4 병렬 (브라우저 리소스 고려)

    # 의존성 있는 테스트 감지: 같은 파일에 여러 함수가 있으면 순서 보장 필요
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
    if HEAL_CONTEXT_PATH.exists():
        try:
            prev = json.loads(HEAL_CONTEXT_PATH.read_text(encoding="utf-8"))
            heal_count = prev.get("heal_count", 0)
        except Exception:
            pass

    # pytest 대상 경로 결정
    if args.group:
        test_targets = [str(GENERATED_DIR / g) for g in args.group]
    else:
        test_targets = [str(GENERATED_DIR)]

    # 2. pytest 실행
    import tempfile
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_report_path = Path(tempfile.gettempdir()) / f"qa_report_{ts}.json"

    subprocess.run(
        [sys.executable, "-m", "pytest"] + test_targets + [
            f"-n{n_workers}",
            f"--dist={dist_mode}",
            "--json-report",
            f"--json-report-file={json_report_path}",
            "--tb=short", "-v",
        ],
        cwd=str(PROJECT_ROOT),
        capture_output=False,
    )
    report = {}
    if json_report_path.exists():
        report = json.loads(json_report_path.read_text(encoding="utf-8"))
        json_report_path.unlink()

    # 3. 결과 파싱
    test_results = parse_results(report)
    pytest_summary = report.get("summary", {})

    # 3-b. 실패 시 heal_context 저장 (Claude Code 힐링 루프용)
    failed_count = pytest_summary.get("failed", 0) + pytest_summary.get("error", 0)
    if failed_count > 0:
        if heal_count >= MAX_HEAL:
            print(f"\n[99] 최대 힐링 횟수({MAX_HEAL}회) 초과 — 수동 수정이 필요합니다.")
            HEAL_CONTEXT_PATH.unlink(missing_ok=True)
        else:
            heal_count += 1
            heal_ctx = build_heal_context(report, heal_count)
            if heal_ctx:
                print_heal_instructions(heal_ctx)
    else:
        # 전체 통과 시 heal_context 정리
        HEAL_CONTEXT_PATH.unlink(missing_ok=True)

    # 4. HTML 리포트
    report_dir = PROJECT_ROOT / "tests" / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    index_path = report_dir / f"parallel_index_{ts}.html"
    index_path.write_text(
        build_html(batch_state, test_results, pytest_summary, now, collected),
        encoding="utf-8"
    )

    # 5. workers 비우기
    workers_dir = PROJECT_ROOT / "workers"
    if workers_dir.exists():
        shutil.rmtree(workers_dir)
        workers_dir.mkdir()
        print("\n[99] workers/ cleared.")

    # 6. 요약 출력
    passed = pytest_summary.get("passed", 0)
    failed = pytest_summary.get("failed", 0) + pytest_summary.get("error", 0)
    print()
    print("=" * 60)
    print("  QA Report Generated")
    print("=" * 60)
    print(f"  Total  : {passed + failed}")
    print(f"  Passed : {passed}")
    print(f"  Failed : {failed}")
    print()
    print(f"  Tests  : {GENERATED_DIR}")
    print(f"  Report : {index_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
