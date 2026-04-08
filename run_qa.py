"""
QA 자동화 진입점.

사용법:
  python run_qa.py --url https://example.com/login --cases config/cases.json

케이스 파일 형식 (두 가지 모두 지원):

  [형식 A] 자연어 문자열 배열 — Claude Code가 DOM 분석 후 steps/assertion 자동 추론
    [
      "정상 로그인이 성공해야 한다",
      "잘못된 비밀번호 입력 시 에러 메시지가 표시되어야 한다"
    ]

  [형식 B] 구조화 객체 배열 — title/steps/expected 직접 지정
    [
      {
        "title": "정상 로그인 성공",
        "steps": [
          "username 필드에 student 입력",
          "password 필드에 Password123 입력",
          "Submit 버튼 클릭"
        ],
        "expected": "Logged In Successfully 텍스트가 표시되어야 한다"
      }
    ]

  [형식 C] 혼합 — 문자열과 객체를 함께 사용 가능
    [
      "잘못된 비밀번호 입력 시 에러 메시지 확인",
      {
        "title": "정상 로그인 성공",
        "steps": ["student 입력", "Password123 입력", "Submit 클릭"],
        "expected": "Logged In Successfully 표시"
      }
    ]
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent / "scripts"))
from parse_cases import load_cases

PROJECT_ROOT = Path(__file__).parent


def init_state(url: str, test_cases: list) -> dict:
    return {
        "url": url,
        "test_cases": test_cases,
        "step": "init",
        "created_at": datetime.now().isoformat(),
        "dom_info": None,
        "plan": None,
        "generated_file_path": "tests/generated/test_generated.py",
        "generated_code": None,
        "lint_result": None,
        "review_summary": None,
        "approval_status": None,
        "rejection_reason": None,
        "rejection_count": 0,
        "execution_result": None,
        "heal_count": 0,
        "heal_context": None,
    }


def print_cases(test_cases: list):
    for i, c in enumerate(test_cases, 1):
        tag = "[구조화]" if c["format"] == "structured" else "[자연어]"
        print(f"    {i}. {tag} {c['title']}")
        if c["format"] == "structured":
            for j, s in enumerate(c["steps"], 1):
                print(f"         step{j}. {s}")
            if c["expected"]:
                print(f"         기대결과: {c['expected']}")


def run_single(url: str, test_cases: list):
    """단일 파이프라인: state.json 생성 후 Claude Code에 실행 지시 출력."""
    natural_count    = sum(1 for c in test_cases if c["format"] == "natural")
    structured_count = sum(1 for c in test_cases if c["format"] == "structured")

    state = init_state(url, test_cases)
    (PROJECT_ROOT / "state.json").write_text(
        json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print("=" * 55)
    print("  QA 자동화 파이프라인 초기화 완료 [단일 모드]")
    print("=" * 55)
    print(f"  URL   : {url}")
    print(f"  케이스 : {len(test_cases)}개  (자연어 {natural_count} / 구조화 {structured_count})")
    print_cases(test_cases)
    print()
    print("  state.json 생성 완료.")
    print()
    print("  -- Claude Code에 아래 메시지를 붙여넣으세요 --")
    print()
    print("  CLAUDE.md 파이프라인대로 QA 자동화를 실행해줘.")
    print("  state.json이 준비되어 있어.")
    print("  01_analyze -> 전략수립 -> 코드작성 ->")
    print("  03_lint -> 요약작성 -> 04_approve -> 05_execute -> 06_heal 순서로 진행해줘.")
    print("=" * 55)


def run_parallel(url: str, test_cases: list, cases_path: Path):
    """병렬 파이프라인: 케이스별 worker 생성 후 batch 실행 지시 출력."""
    tmp_dir = PROJECT_ROOT / "testcases" / ".auto"
    tmp_dir.mkdir(parents=True, exist_ok=True)

    # 기존 .auto 파일 정리
    for f in tmp_dir.glob("case_*.json"):
        f.unlink()

    # base_group: testcases/login/cases.md → "login"
    parent = cases_path.parent.name
    base_group = parent if parent not in ("testcases", "config", ".") else cases_path.stem

    targets = []
    for i, case in enumerate(test_cases):
        case_file = tmp_dir / f"case_{i:03d}.json"
        case_file.write_text(json.dumps([case], ensure_ascii=False), encoding="utf-8")
        targets.append({"url": url, "cases": str(case_file),
                        "base_group": base_group, "case_index": i})

    targets_file = tmp_dir / "targets_auto.json"
    targets_file.write_text(json.dumps(targets, ensure_ascii=False), encoding="utf-8")

    print("=" * 55)
    print("  QA 자동화 파이프라인 초기화 완료 [병렬 모드]")
    print("=" * 55)
    print(f"  URL   : {url}")
    print(f"  케이스 : {len(test_cases)}개 -> worker {len(test_cases)}개 병렬 실행")
    print_cases(test_cases)
    print()
    print(f"  Worker 환경 초기화 중 (DOM 분석 포함)...")
    print()

    split_script = PROJECT_ROOT / "parallel" / "00_split.py"
    result = subprocess.run(
        [sys.executable, str(split_script), "--targets", str(targets_file)],
        cwd=str(PROJECT_ROOT),
    )
    if result.returncode != 0:
        print("[오류] worker 초기화 실패.")
        sys.exit(1)

    batch_state_path = PROJECT_ROOT / "parallel" / "batch_state.json"
    if not batch_state_path.exists():
        print("[오류] batch_state.json 생성 실패.")
        sys.exit(1)

    batch_state = json.loads(batch_state_path.read_text(encoding="utf-8"))
    workers = batch_state.get("workers", [])

    print()
    print("=" * 55)
    print(f"  batch_state.json 생성 완료 - {len(workers)}개 worker")
    print("=" * 55)
    print()
    print("  -- Claude Code에 아래 메시지를 붙여넣으세요 --")
    print()
    print("  CLAUDE.md 병렬 파이프라인대로 QA 자동화를 실행해줘.")
    print("  parallel/batch_state.json이 준비되어 있어.")
    print("  아래 worker를 Agent tool로 모두 동시에 실행해줘:")
    print()
    for w in workers:
        print(f"    worker_dir : {w['worker_dir']}")
        print(f"    group_dir  : {w.get('group_dir', w['group_label'])}")
        print(f"    group_label: {w['group_label']}")
        print(f"    케이스수   : {w['case_count']}개")
        print()
    print("  모든 worker 완료 후:")
    print("  python parallel/99_merge.py 실행")
    print("=" * 55)


def main():
    parser = argparse.ArgumentParser(description="QA 자동화 파이프라인 시작")
    parser.add_argument("--url",   required=True, help="테스트 대상 URL")
    parser.add_argument("--cases", default=None,  help="테스트 케이스 파일 경로 (.md 또는 .json)")
    args = parser.parse_args()

    if args.cases and Path(args.cases).exists():
        test_cases = load_cases(args.cases)
    else:
        print("[오류] --cases 옵션으로 케이스 파일을 지정하세요. (.md 또는 .json)")
        sys.exit(1)

    if len(test_cases) == 1:
        run_single(args.url, test_cases)
    else:
        run_parallel(args.url, test_cases, Path(args.cases))


if __name__ == "__main__":
    main()
