"""
UserPromptSubmit 훅에서 실행됨.
state/discuss.json의 step=pending이면 팀 토론 시작 요청을 stdout으로 출력해
Claude 컨텍스트에 주입한다.
"""
import sys
from _paths import DISCUSS_STATE
from hook_utils import check_state

state = check_state(DISCUSS_STATE, key="step", value="pending")
if state is None:
    sys.exit(0)

topic = state.get("topic", "")
rejection_reason = state.get("rejection_reason", "")

lines = [
    "[팀 토론 자동 시작] state/discuss.json에 pending 토론이 있습니다. 즉시 팀 토론을 진행해주세요.",
    f"주제: {topic}",
]
if rejection_reason:
    lines.append(f"재토론 사유: {rejection_reason}")

lines += [
    "",
    "진행 방법: CLAUDE.md의 '팀 자유 토론 파이프라인' 지침을 따라 실행하세요.",
    "1. python scripts/team_discuss.py 실행",
    "2. 출력의 DELIBERATION_CONTEXT_START ~ END 사이 JSON 추출",
    "3. 멀티라운드 티키타카 진행 (최소 3라운드, 발언마다 agents/dialog.json에 즉시 append)",
    "4. 완료 후 state/discuss.json step='discussed', conclusion 저장",
]

print("\n".join(lines))
