"""
QA 병렬 자동화 진입점.

URL별로 독립된 worker 환경을 구성하고,
Claude Code의 Agent tool이 각 URL을 동시에 처리하도록 지시한다.

사용법:
  # URL 자동 감지 (config/pages.json + testcases/ 폴더 스캔)
  python run_qa_parallel.py

  # 특정 targets.json 지정
  python run_qa_parallel.py --targets testcases/targets_demo.json

targets.json 형식 (url 생략 시 config/pages.json에서 자동 조회):
  [
    { "url": "https://site.com/login", "cases": "testcases/login" },
    { "cases": "testcases/checkout" }   ← url 생략 가능
  ]
"""
import json
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
PAGES_JSON = PROJECT_ROOT / "config" / "pages.json"


def main():
    import argparse
    parser = argparse.ArgumentParser(description="QA 병렬 파이프라인 시작")
    parser.add_argument("--targets", default=None,
                        help="targets.json 경로. 생략 시 testcases/ 폴더 자동 스캔.")
    args = parser.parse_args()

    print("=" * 60)
    print("  QA 병렬 파이프라인 시작")
    print("=" * 60)

    # pages.json 로드해서 등록된 URL 표시
    if PAGES_JSON.exists():
        pages = json.loads(PAGES_JSON.read_text(encoding="utf-8"))
        active = {k: v for k, v in pages.items() if v}
        print(f"  config/pages.json — {len(active)}개 페이지 등록됨")
        for name, url in active.items():
            print(f"    [{name}] {url}")
    print()

    # 00_split.py 호출 → worker 디렉토리 생성 + DOM 분석
    split_script = PROJECT_ROOT / "parallel" / "00_split.py"
    split_cmd = [sys.executable, str(split_script)]
    if args.targets:
        split_cmd += ["--targets", args.targets]

    result = subprocess.run(split_cmd, capture_output=False)
    if result.returncode != 0:
        print("[오류] 배치 분할 실패.")
        sys.exit(1)

    # batch_state.json 읽어 worker 목록 출력
    batch_state_path = Path("parallel/batch_state.json")
    if not batch_state_path.exists():
        print("[오류] batch_state.json 생성 실패.")
        sys.exit(1)

    batch_state = json.loads(batch_state_path.read_text(encoding="utf-8"))
    workers = batch_state["workers"]

    print()
    print("=" * 60)
    print("  worker 준비 완료")
    print("=" * 60)
    for w in workers:
        print(f"  [{w['worker_id']}] {w['url']}")
        print(f"    디렉토리 : {w['worker_dir']}")
        print(f"    케이스   : {w['case_count']}개")
        print()

    print("=" * 60)
    print("  -- Claude Code에 아래 지시를 전달하세요 --")
    print("=" * 60)
    print()
    print("  parallel/batch_state.json 의 workers 목록을 읽고")
    print("  각 worker를 Agent tool로 동시에 실행해줘.")
    print()
    print("  각 subagent에게 전달할 지시:")
    print("  CLAUDE.md 병렬 파이프라인 섹션의 Subagent 지시 형식을 따를 것.")
    print()
    print("  전체 완료 후:")
    print("  python parallel/99_merge.py 를 실행해 결과를 병합할 것.")
    print("=" * 60)


if __name__ == "__main__":
    main()
