"""
UserPromptSubmit 훅에서 실행됨.
pending_impl.json이 있으면 구현 요청을 stdout으로 출력해 Claude 컨텍스트에 주입한다.
"""
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
PENDING_PATH = PROJECT_ROOT / "pending_impl.json"

if not PENDING_PATH.exists():
    sys.exit(0)

try:
    data = json.loads(PENDING_PATH.read_text(encoding="utf-8"))
except Exception:
    sys.exit(0)

if data.get("status") != "pending":
    sys.exit(0)

items = data.get("items", [])
topic = data.get("topic", "")
approved = [i for i in items if i.get("status") == "approved"]

if not approved:
    sys.exit(0)

lines = [
    f"[자동 구현 요청] 팀 토론 승인 항목이 있습니다. 즉시 구현해주세요.",
    f"주제: {topic}",
    "",
    "승인된 항목:"
]
for item in approved:
    lines.append(f"- {item['title']}: {item['text']}")

lines += [
    "",
    "구현 완료 후 반드시 다음을 실행하세요:",
    "1. pending_impl.json 삭제 (또는 status를  'done'으로 변경)",
    "2. agents/team_notes.md 초기화 (헤더만 남김)",
    "3. discuss_state.json 초기화 (step: 'idle')",
]

print("\n".join(lines))
