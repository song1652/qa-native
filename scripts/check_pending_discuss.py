"""
UserPromptSubmit 훅에서 실행됨.
discuss_state.json의 step=pending이면 팀 토론 시작 요청을 stdout으로 출력해
Claude 컨텍스트에 주입한다.
"""
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
DISCUSS_PATH = PROJECT_ROOT / "discuss_state.json"

if not DISCUSS_PATH.exists():
    sys.exit(0)

try:
    data = json.loads(DISCUSS_PATH.read_text(encoding="utf-8"))
except Exception:
    sys.exit(0)

if data.get("step") != "pending":
    sys.exit(0)

topic = data.get("topic", "")
rejection_reason = data.get("rejection_reason", "")

lines = [
    "[팀 토론 자동 시작] discuss_state.json에 pending 토론이 있습니다. 즉시 팀 토론을 진행해주세요.",
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
    "4. 완료 후 discuss_state.json step='discussed', conclusion 저장",
]

print("\n".join(lines))
