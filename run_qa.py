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
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent / "scripts"))
from parse_cases import load_cases
from _paths import PIPELINE_STATE, STATE_DIR


def init_state(url: str, test_cases: list, cases_path: str) -> dict:
    p = Path(cases_path)
    group_dir = p.name if p.is_dir() else p.parent.name
    return {
        "url": url,
        "test_cases": test_cases,
        "step": "init",
        "created_at": datetime.now().isoformat(),
        "cases_path": str(cases_path),
        "group_dir": group_dir,
        "dom_info": None,
        "plan": None,
        "generated_file_path": f"tests/generated/{group_dir}/",
        "generated_files": [],
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


def run_single(url: str, test_cases: list, cases_path: str):
    """단일 파이프라인: state/pipeline.json 생성 후 Claude Code에 실행 지시 출력."""
    natural_count    = sum(1 for c in test_cases if c["format"] == "natural")
    structured_count = sum(1 for c in test_cases if c["format"] == "structured")

    state = init_state(url, test_cases, cases_path)
    STATE_DIR.mkdir(exist_ok=True)
    PIPELINE_STATE.write_text(
        json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print("=" * 55)
    print("  QA 자동화 파이프라인 초기화 완료 [단일 모드]")
    print("=" * 55)
    print(f"  URL   : {url}")
    print(f"  케이스 : {len(test_cases)}개  (자연어 {natural_count} / 구조화 {structured_count})")
    print_cases(test_cases)
    print()
    print("  state/pipeline.json 생성 완료.")
    print()
    print("  -- Claude Code에 아래 메시지를 붙여넣으세요 --")
    print()
    print("  CLAUDE.md 파이프라인대로 QA 자동화를 실행해줘.")
    print("  state/pipeline.json이 준비되어 있어.")
    print("  01_analyze -> 전략수립 -> 코드작성 ->")
    print("  03_lint -> 요약작성 -> 04_approve -> 05_execute -> 06_heal 순서로 진행해줘.")
    print("=" * 55)


def main():
    parser = argparse.ArgumentParser(description="QA 자동화 파이프라인 시작 (단일 모드)")
    parser.add_argument("--url",   required=True, help="테스트 대상 URL")
    parser.add_argument("--cases", default=None,  help="테스트 케이스 파일 경로 (.md 또는 .json)")
    args = parser.parse_args()

    if args.cases and Path(args.cases).exists():
        test_cases = load_cases(args.cases)
    else:
        print("[오류] --cases 옵션으로 케이스 파일을 지정하세요. (.md 또는 .json)")
        sys.exit(1)

    run_single(args.url, test_cases, args.cases)


if __name__ == "__main__":
    main()
