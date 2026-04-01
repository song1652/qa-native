"""
팀 자유 토론 진입점.

사용법:
  python run_team.py --topic "테스트 케이스 작성 기준"
  python run_team.py  (주제를 대화형으로 입력)
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "scripts"))
from _paths import DISCUSS_STATE, STATE_DIR

DISCUSS_STATE_PATH = DISCUSS_STATE


def main():
    import argparse
    parser = argparse.ArgumentParser(description="팀 자유 토론 시작")
    parser.add_argument("--topic", "-t", default=None, help="토론 주제")
    args = parser.parse_args()

    topic = args.topic
    if not topic:
        print("=" * 60)
        print("  QA 팀 자유 토론")
        print("=" * 60)
        topic = input("  토론 주제를 입력하세요: ").strip()
        if not topic:
            print("[오류] 주제를 입력해야 합니다.")
            sys.exit(1)

    # state/discuss.json 초기화
    discuss_state = {
        "topic": topic,
        "step": "init",
        "conclusion": "",
        "rejection_reason": "",
        "rejection_count": 0,
        "created_at": __import__("datetime").datetime.now().isoformat(),
    }
    DISCUSS_STATE_PATH.write_text(
        json.dumps(discuss_state, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print()
    print("=" * 60)
    print("  팀 토론 시작")
    print("=" * 60)
    print(f"  주제: {topic}")
    print()
    print("  다음 단계를 순서대로 실행하세요:")
    print()
    print("  1. python scripts/team_discuss.py")
    print("     출력의 DELIBERATION_CONTEXT JSON을 추출해 심의 agent 호출")
    print()
    print("  2. [심의 Agent] 사수/부사수 토론 실행")
    print("     → state/discuss.json에 conclusion 저장")
    print("     → agents/dialog.json 마지막 session 업데이트")
    print()
    print("  3. python scripts/team_approve.py")
    print("     결론 검토 후 y/n 승인")
    print("=" * 60)


if __name__ == "__main__":
    main()
