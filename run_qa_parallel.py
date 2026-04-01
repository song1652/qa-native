"""
QA 병렬 자동화 진입점 (간소화).

testcases/ 폴더를 스캔하고 URL별 DOM 분석 후,
Claude Code subagent에 전달할 컨텍스트를 출력한다.
worker 디렉토리 없이 subagent가 tests/generated/에 직접 저장.

사용법:
  # 전체 자동 스캔 (config/pages.json + testcases/ 폴더)
  python run_qa_parallel.py

  # 특정 폴더만
  python run_qa_parallel.py --folders login saintcore

  # targets.json 지정
  python run_qa_parallel.py --targets testcases/targets_demo.json
"""
import argparse
import asyncio
import json
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent / "scripts"))
from parse_cases import load_cases
from _paths import PROJECT_ROOT, PARALLEL_STATE, STATE_DIR

# 01_analyze.py의 analyze() 직접 import
from importlib import import_module as _im

PAGES_JSON = PROJECT_ROOT / "config" / "pages.json"
TEST_DATA_JSON = PROJECT_ROOT / "config" / "test_data.json"
PARALLEL_STATE_PATH = PARALLEL_STATE


def _save_state(state: dict) -> None:
    """state/parallel.json에 상태 저장 (기존 상태와 병합)."""
    existing = {}
    if PARALLEL_STATE_PATH.exists():
        try:
            existing = json.loads(PARALLEL_STATE_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    existing.update(state)
    PARALLEL_STATE_PATH.write_text(
        json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def load_pages() -> dict:
    if PAGES_JSON.exists():
        return json.loads(PAGES_JSON.read_text(encoding="utf-8"))
    return {}


def load_test_data() -> dict:
    if TEST_DATA_JSON.exists():
        return json.loads(TEST_DATA_JSON.read_text(encoding="utf-8"))
    return {}


def resolve_url(folder_name: str, pages: dict) -> str | None:
    return pages.get(folder_name) or None


def read_file_safe(path: Path) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""


def analyze_url(url: str) -> dict:
    """01_analyze.py의 analyze() 함수를 직접 호출해 DOM 분석."""
    spec = _im("importlib.util").find_spec(
        "01_analyze",
        [str(PROJECT_ROOT / "scripts")],
    )
    if spec is None:
        # fallback: 직접 import
        analyze_mod_path = PROJECT_ROOT / "scripts" / "01_analyze.py"
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "analyze_mod", str(analyze_mod_path)
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    else:
        import importlib.util
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    return asyncio.run(mod.analyze(url))


def resolve_targets(args, pages: dict) -> list[dict]:
    """실행 대상 목록 생성. 각 항목: {url, cases_path, group_dir, group_label}"""
    targets = []

    if args.targets:
        targets_path = Path(args.targets)
        if not targets_path.exists():
            print(f"[오류] targets 파일 없음: {args.targets}")
            sys.exit(1)
        raw = json.loads(targets_path.read_text(encoding="utf-8"))
        for t in raw:
            url = t.get("url")
            cases = t["cases"]
            if not url:
                folder = Path(cases).name
                url = pages.get(folder) or pages.get(Path(cases).parent.name)
            if not url:
                print(f"[건너뜀] URL 없음: {cases}")
                continue
            targets.append({"url": url, "cases": cases})
        return _expand_targets(targets)

    # 폴더 자동 스캔
    testcases_root = PROJECT_ROOT / "testcases"
    if not testcases_root.exists():
        print("[오류] testcases/ 폴더 없음.")
        sys.exit(1)

    folder_filter = args.folders if args.folders else None

    for folder in sorted(testcases_root.iterdir()):
        if not folder.is_dir() or folder.name.startswith("."):
            continue
        if folder_filter and folder.name not in folder_filter:
            continue
        url = resolve_url(folder.name, pages)
        if not url:
            print(f"[건너뜀] '{folder.name}' — config/pages.json에 URL 없음")
            continue
        targets.append({
            "url": url,
            "cases": str(folder),
            "base_group": folder.name,
        })

    if not targets:
        print("[오류] 실행할 대상 없음. config/pages.json에 URL을 등록하세요.")
        sys.exit(1)

    return _expand_targets(targets)


def _expand_targets(targets: list[dict]) -> list[dict]:
    """폴더 내 tc_*.md 파일을 개별 타겟으로 확장."""
    expanded = []
    for target in targets:
        cases_path = Path(target["cases"])
        if not cases_path.is_absolute():
            cases_path = PROJECT_ROOT / cases_path

        base_group = target.get("base_group")
        if not base_group:
            parent = cases_path.parent.name
            base_group = parent if parent not in ("testcases", "config", ".") else cases_path.stem

        if cases_path.is_dir():
            md_files = sorted(cases_path.glob("tc_*.md"))
            if not md_files:
                md_files = sorted(cases_path.glob("*.md"))
            if not md_files:
                print(f"[경고] 폴더에 .md 파일 없음: {cases_path}")
                continue
            for j, md in enumerate(md_files):
                expanded.append({
                    "url": target["url"],
                    "cases_path": md,
                    "group_dir": base_group,
                    "group_label": md.stem,  # tc_01_login_success
                })
        else:
            expanded.append({
                "url": target["url"],
                "cases_path": cases_path,
                "group_dir": base_group,
                "group_label": cases_path.stem,
            })

    return expanded


def main():
    parser = argparse.ArgumentParser(description="QA 병렬 파이프라인 (간소화)")
    parser.add_argument("--targets", default=None,
                        help="targets.json 경로. 생략 시 testcases/ 폴더 자동 스캔.")
    parser.add_argument("--folders", nargs="*", default=None,
                        help="특정 폴더만 실행 (예: login saintcore)")
    args = parser.parse_args()

    pages = load_pages()
    test_data = load_test_data()

    print("=" * 60)
    print("  QA 병렬 파이프라인 시작 (간소화)")
    print("=" * 60)

    # 상태 파일 초기화
    parallel_dir = PROJECT_ROOT / "parallel"
    parallel_dir.mkdir(exist_ok=True)
    STATE_DIR.mkdir(exist_ok=True)
    _save_state({"status": "init", "created_at": datetime.now().isoformat()})

    # 등록된 페이지 표시
    active = {k: v for k, v in pages.items() if v}
    print(f"  config/pages.json — {len(active)}개 페이지 등록")
    for name, url in active.items():
        print(f"    [{name}] {url}")
    print()

    # 1. 대상 목록 생성
    targets = resolve_targets(args, pages)
    print(f"[준비] {len(targets)}개 대상 확인")

    # 2. URL별 DOM 분석 (캐시)
    _save_state({"status": "analyzing",
                 "created_at": datetime.now().isoformat(),
                 "total_count": len(targets)})
    unique_urls = list(dict.fromkeys(t["url"] for t in targets))
    dom_cache: dict[str, dict] = {}

    for url in unique_urls:
        print(f"[DOM] 분석 중: {url}")
        dom_cache[url] = analyze_url(url)
        dom = dom_cache[url]
        if "error" in dom:
            print(f"  [경고] DOM 분석 실패: {dom['error']}")
        else:
            print(f"  완료 — 입력:{len(dom.get('inputs',[]))} 버튼:{len(dom.get('buttons',[]))}")

    # 3. 컨텍스트 파일 1회 읽기
    team_charter = read_file_safe(PROJECT_ROOT / "agents" / "team_charter.md")
    lessons_learned = read_file_safe(PROJECT_ROOT / "agents" / "lessons_learned.md")

    # 4. subagent 컨텍스트 빌드
    contexts = []
    for t in targets:
        cases = load_cases(str(t["cases_path"]))
        page_key = t["group_dir"]
        output_dir = PROJECT_ROOT / "tests" / "generated" / t["group_dir"]
        output_dir.mkdir(parents=True, exist_ok=True)

        ctx = {
            "group_dir": t["group_dir"],
            "group_label": t["group_label"],
            "url": t["url"],
            "dom_info": dom_cache.get(t["url"], {}),
            "test_cases": cases,
            "test_data": test_data.get(page_key, {}),
            "team_charter": team_charter,
            "lessons_learned": lessons_learned,
            "output_path": f"tests/generated/{t['group_dir']}/{t['group_label']}.py",
        }
        contexts.append(ctx)
        print(f"  [{t['group_label']}] {len(cases)}개 케이스 → {ctx['output_path']}")

    # 5. 상태 파일 저장 (ready = subagent 대기)
    _save_state({
        "status": "ready",
        "total_count": len(contexts),
        "completed_count": 0,
        "targets": [
            {
                "group_dir": c["group_dir"],
                "group_label": c["group_label"],
                "url": c["url"],
                "output_path": c["output_path"],
                "case_count": len(c["test_cases"]),
            }
            for c in contexts
        ],
    })

    # 6. subagent 컨텍스트 출력
    print()
    print("=== PARALLEL_SUBAGENT_CONTEXTS_START ===")
    print(json.dumps(contexts, ensure_ascii=False, indent=2))
    print("=== PARALLEL_SUBAGENT_CONTEXTS_END ===")
    print()

    print("=" * 60)
    print("  Claude Code에 아래 지시를 전달하세요:")
    print("=" * 60)
    print()
    print("  위 PARALLEL_SUBAGENT_CONTEXTS의 각 항목을 Agent tool로 동시에 실행해줘.")
    print()
    print("  각 subagent는:")
    print("  1. 컨텍스트의 dom_info와 test_cases를 바탕으로 plan 수립")
    print("  2. plan 기반으로 Playwright 테스트 코드 작성")
    print("  3. output_path에 직접 저장")
    print()
    print("  완료 후: python parallel/99_merge.py 실행")
    print("=" * 60)


if __name__ == "__main__":
    main()
