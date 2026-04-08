"""
병렬 파이프라인 Step 0 — URL별 worker 환경 초기화

targets.json의 각 URL에 대해:
  1. workers/{worker_id}/ 독립 디렉토리 생성
  2. DOM 분석 (01_analyze.py) 실행 → dom_info 수집
  3. state.json 초기화 (step="analyzed" 상태로, dom_info 포함)
  4. tests/ 하위 디렉토리 + conftest.py 복사
  5. parallel/batch_state.json 생성

LLM 없음. 순수 Python + Playwright.
"""
import json
import subprocess
import sys
import shutil
import re
from pathlib import Path
from datetime import datetime

# 프로젝트 루트 (이 스크립트 기준 상위 디렉토리)
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
from parse_cases import load_cases

PAGES_JSON = PROJECT_ROOT / "config" / "pages.json"


def load_pages() -> dict:
    """config/pages.json 로드. 없으면 빈 dict 반환."""
    if PAGES_JSON.exists():
        return json.loads(PAGES_JSON.read_text(encoding="utf-8"))
    return {}


def resolve_url(target: dict, pages: dict) -> str:
    """target에서 URL 결정. url 필드 없으면 cases 폴더명으로 pages.json 조회."""
    if target.get("url"):
        return target["url"]
    # cases 경로에서 폴더명 추출 → pages.json 키로 사용
    folder = Path(target["cases"]).name
    if folder in pages and pages[folder]:
        return pages[folder]
    # cases 파일의 부모 폴더명 시도
    parent = Path(target["cases"]).parent.name
    if parent in pages and pages[parent]:
        return pages[parent]
    raise ValueError(
        f"URL을 찾을 수 없습니다: '{folder}'\n"
        f"  → config/pages.json에 '{folder}' 키를 추가해 주세요."
    )


def slugify_url(url: str) -> str:
    """URL을 파일시스템에 안전한 디렉토리명으로 변환."""
    # http(s):// 제거 후 특수문자를 _로 치환
    slug = re.sub(r"https?://", "", url)
    slug = re.sub(r"[^\w]", "_", slug).strip("_")
    return slug[:40]  # 최대 40자




def run_analyze(worker_dir: Path, url: str) -> dict:
    """01_analyze.py를 worker_dir을 cwd로 실행해 dom_info를 수집한다."""
    # worker_dir에 임시 state.json 생성 (url만 있으면 됨)
    temp_state = {
        "url": url,
        "test_cases": [],
        "step": "init",
        "dom_info": None,
    }
    (worker_dir / "state.json").write_text(
        json.dumps(temp_state, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    analyze_script = PROJECT_ROOT / "scripts" / "01_analyze.py"
    result = subprocess.run(
        [sys.executable, str(analyze_script)],
        cwd=str(worker_dir),
        capture_output=True,
        text=True,
    )

    print(result.stdout)
    if result.returncode != 0:
        print(f"[경고] DOM 분석 실패: {url}")
        print(result.stderr)
        return {}

    state = json.loads((worker_dir / "state.json").read_text(encoding="utf-8"))
    return state.get("dom_info", {})


def init_worker(worker_dir: Path, url: str, test_cases: list, dom_info: dict):
    """worker_dir의 state.json을 완전히 초기화한다 (step=analyzed)."""
    state = {
        "url": url,
        "test_cases": test_cases,
        "step": "analyzed",
        "created_at": datetime.now().isoformat(),
        "dom_info": dom_info,
        "plan": None,
        "generated_file_path": "tests/generated/test_generated.py",
        "generated_code": None,
        "lint_result": None,
        "review_summary": None,
        "approval_status": "approved",   # 병렬 모드: 자동 승인
        "rejection_reason": None,
        "rejection_count": 0,
        "execution_result": None,
        "heal_count": 0,
        "heal_context": None,
    }
    (worker_dir / "state.json").write_text(
        json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def setup_worker_dirs(worker_dir: Path):
    """worker 하위 디렉토리 생성 및 conftest.py 복사."""
    for sub in ["tests/generated", "tests/reports", "tests/screenshots"]:
        (worker_dir / sub).mkdir(parents=True, exist_ok=True)

    # conftest.py 복사
    src_conftest = PROJECT_ROOT / "tests" / "conftest.py"
    dst_conftest = worker_dir / "tests" / "conftest.py"
    if src_conftest.exists():
        shutil.copy2(src_conftest, dst_conftest)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--targets", default=None,
                        help="targets.json 경로. 생략 시 testcases/ 폴더 자동 스캔.")
    args = parser.parse_args()

    pages = load_pages()

    if args.targets:
        targets_path = Path(args.targets)
        if not targets_path.exists():
            print(f"[오류] targets 파일 없음: {args.targets}")
            sys.exit(1)
        targets_raw = json.loads(targets_path.read_text(encoding="utf-8"))
        # url 없는 항목은 pages.json에서 조회
        targets = []
        for t in targets_raw:
            url = resolve_url(t, pages)
            targets.append({"url": url, "cases": t["cases"],
                            **{k: v for k, v in t.items() if k not in ("url", "cases")}})
    else:
        # testcases/ 폴더 자동 스캔
        testcases_root = PROJECT_ROOT / "testcases"
        if not testcases_root.exists():
            print("[오류] testcases/ 폴더 없음.")
            sys.exit(1)
        targets = []
        for folder in sorted(testcases_root.iterdir()):
            if not folder.is_dir():
                continue
            if folder.name not in pages or not pages[folder.name]:
                print(f"[건너뜀] '{folder.name}' — config/pages.json에 URL 없음")
                continue
            targets.append({"url": pages[folder.name], "cases": str(folder),
                            "base_group": folder.name})
        if not targets:
            print("[오류] 실행할 대상 없음. config/pages.json에 URL을 등록하세요.")
            sys.exit(1)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    workers_root = PROJECT_ROOT / "workers"
    workers_root.mkdir(exist_ok=True)

    batch_workers = []

    # targets 확장: cases가 폴더면 하위 *.md 파일 각각을 개별 target으로 분해
    expanded = []
    for target in targets:
        cases_path = Path(target["cases"])
        if not cases_path.is_absolute():
            cases_path = PROJECT_ROOT / cases_path
        if cases_path.is_dir():
            md_files = sorted(cases_path.glob("*.md"))
            if not md_files:
                print(f"[경고] 폴더에 .md 파일 없음: {cases_path}")
                continue
            for j, md in enumerate(md_files):
                entry = {"url": target["url"], "cases": md}
                if "base_group" in target:
                    entry["base_group"] = target["base_group"]
                    entry["case_index"] = j
                expanded.append(entry)
        else:
            entry = {"url": target["url"], "cases": cases_path}
            if "base_group" in target:
                entry["base_group"] = target["base_group"]
                entry["case_index"] = target.get("case_index", 0)
            expanded.append(entry)

    # URL별 DOM 분석 캐시 (같은 URL은 1회만 분석)
    dom_cache: dict[str, dict] = {}

    for i, target in enumerate(expanded, 1):
        url = target["url"]
        cases_path = Path(target["cases"])

        print(f"\n[00] ({i}/{len(expanded)}) 초기화 중: {url}  [{cases_path.name}]")

        # worker 디렉토리 — 인덱스 포함으로 동일 URL 중복 실행 시 충돌 방지
        slug = slugify_url(url)
        worker_id = f"{i:02d}_{slug}_{ts}"
        worker_dir = workers_root / worker_id
        worker_dir.mkdir(parents=True, exist_ok=True)

        # 하위 디렉토리 + conftest.py
        setup_worker_dirs(worker_dir)

        # 케이스 로드 (.md / .json 자동 선택)
        if not cases_path.exists():
            print(f"[경고] cases 파일 없음: {cases_path}, 건너뜀.")
            continue
        test_cases = load_cases(cases_path)

        # DOM 분석 — 같은 URL이면 캐시 사용
        if url not in dom_cache:
            print(f"[00]   DOM 분석 중...")
            dom_cache[url] = run_analyze(worker_dir, url)
        else:
            print(f"[00]   DOM 캐시 사용 (재분석 생략)")
            # state.json은 run_analyze가 생성하므로, 캐시 사용 시 직접 생성
            temp_state = {"url": url, "test_cases": [], "step": "init", "dom_info": None}
            (worker_dir / "state.json").write_text(
                json.dumps(temp_state, ensure_ascii=False, indent=2), encoding="utf-8"
            )
        dom_info = dom_cache[url]

        # state.json 완전 초기화
        init_worker(worker_dir, url, test_cases, dom_info)

        # group_dir + group_label 결정
        # target에 base_group이 있으면 사용 (run_qa.py 자동 라우팅), 없으면 경로에서 유추
        if "base_group" in target:
            base_group = target["base_group"]
            case_index = target.get("case_index", i - 1)
            group_dir   = base_group
            group_label = f"{base_group}_{case_index:03d}"
        else:
            parent_name = cases_path.parent.name
            group_dir   = parent_name if parent_name not in ("config", "testcases", ".") else cases_path.stem
            group_label = group_dir

        batch_workers.append({
            "worker_id": worker_id,
            "worker_dir": str(worker_dir.relative_to(PROJECT_ROOT)),
            "url": url,
            "cases_file": str(cases_path.relative_to(PROJECT_ROOT)),
            "group_dir":   group_dir,
            "group_label": group_label,
            "case_count": len(test_cases),
            "status": "pending",
            "started_at": None,
            "completed_at": None,
            "result_summary": None,
        })

        print(f"[00]   완료 - {len(test_cases)}개 케이스, worker: {worker_id}")

    # batch_state.json 저장
    batch_state = {
        "created_at": datetime.now().isoformat(),
        "worker_count": len(batch_workers),
        "workers": batch_workers,
    }
    parallel_dir = PROJECT_ROOT / "parallel"
    parallel_dir.mkdir(exist_ok=True)
    (parallel_dir / "batch_state.json").write_text(
        json.dumps(batch_state, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"\n[00] 전체 초기화 완료 - {len(batch_workers)}개 worker 준비됨")
    print(f"[00] batch_state.json 저장: parallel/batch_state.json")


if __name__ == "__main__":
    main()
