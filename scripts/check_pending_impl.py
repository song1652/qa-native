"""
UserPromptSubmit 훅에서 실행됨.
pending_impl.json이 있으면 구현 요청을 stdout으로 출력해 Claude 컨텍스트에 주입한다.
"""
import sys
from _paths import PROJECT_ROOT
from hook_utils import check_state

PENDING_PATH = PROJECT_ROOT / "pending_impl.json"


def _has_approved_items(s: dict) -> bool:
    approved = [i for i in s.get("items", []) if i.get("status") == "approved"]
    return bool(approved)


state = check_state(PENDING_PATH, key="status", value="pending", extra_check=_has_approved_items)
if state is None:
    sys.exit(0)

items = state.get("items", [])
topic = state.get("topic", "")
approved = [i for i in items if i.get("status") == "approved"]

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
    "3. state/discuss.json 초기화 (step: 'idle')",
    "4. agents/dialog.json 마지막 세션의 status를 'approved', completed_at를 현재시각으로 업데이트",
]

print("\n".join(lines))
