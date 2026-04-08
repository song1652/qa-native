"""
팀 토론 결론 승인
사용자에게 결론을 보여주고 y/n 승인을 받는다.
승인 시 agents/team_notes.md에 저장.
반려 시 rejection_reason 저장 후 종료코드 1.
"""
import json
import sys
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent
DISCUSS_STATE_PATH = PROJECT_ROOT / "discuss_state.json"
TEAM_NOTES_PATH = PROJECT_ROOT / "agents" / "team_notes.md"
DIALOG_PATH = PROJECT_ROOT / "agents" / "dialog.json"


def append_to_notes(topic: str, conclusion: str):
    today = datetime.now().strftime("%Y-%m-%d")
    section = f"\n## {topic}\n> 결정일: {today}\n\n{conclusion}\n\n---\n"
    if TEAM_NOTES_PATH.exists():
        existing = TEAM_NOTES_PATH.read_text(encoding="utf-8")
    else:
        existing = "# 팀 결정 사항\n\n---\n"
    TEAM_NOTES_PATH.write_text(existing + section, encoding="utf-8")


def main():
    if not DISCUSS_STATE_PATH.exists():
        print("[오류] discuss_state.json 없음.")
        sys.exit(1)

    discuss = json.loads(DISCUSS_STATE_PATH.read_text(encoding="utf-8"))
    topic = discuss.get("topic", "")
    conclusion = discuss.get("conclusion", "")

    if not conclusion:
        print("[오류] 결론 없음. 심의 agent가 discuss_state.json에 conclusion을 저장해야 합니다.")
        sys.exit(1)

    print("=" * 60)
    print(f"  팀 토론 결론 검토")
    print("=" * 60)
    print(f"  주제: {topic}")
    print()
    print(conclusion)
    print()
    print("=" * 60)

    answer = input("  이 결론을 승인하시겠습니까? (y/n): ").strip().lower()

    if answer == "y":
        append_to_notes(topic, conclusion)
        discuss["step"] = "approved"
        discuss["rejection_reason"] = ""
        DISCUSS_STATE_PATH.write_text(
            json.dumps(discuss, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print()
        print(f"  저장 완료: agents/team_notes.md")
        print("=" * 60)
        sys.exit(0)
    else:
        reason = input("  반려 사유 (Enter 시 생략): ").strip()
        discuss["step"] = "rejected"
        discuss["rejection_reason"] = reason
        discuss["rejection_count"] = discuss.get("rejection_count", 0) + 1
        DISCUSS_STATE_PATH.write_text(
            json.dumps(discuss, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print()
        print("  반려됨. 재토론을 진행합니다.")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    main()
