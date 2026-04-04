"""
UserPromptSubmit 훅에서 실행됨.
state/pipeline.json의 step=approved이고 execution_result가 없으면
대시보드에서 승인된 것이므로 파이프라인 실행을 Claude에 요청한다.
"""
import json
import sys
from _paths import PIPELINE_STATE, read_state

STATE_PATH = PIPELINE_STATE

if not STATE_PATH.exists():
    sys.exit(0)

try:
    state = read_state(STATE_PATH)
except Exception:
    sys.exit(0)

# 대시보드에서 승인했지만 아직 실행 안 된 경우만
if state.get("step") != "approved":
    sys.exit(0)

if state.get("execution_result"):
    sys.exit(0)

url = state.get("url", "")
case_count = len(state.get("test_cases", []))

lines = [
    "[파이프라인 자동 실행] 대시보드에서 승인이 완료되었습니다.",
    f"URL: {url}",
    f"케이스: {case_count}개",
    "",
    "CLAUDE.md 파이프라인의 7번 단계부터 실행해주세요:",
    "1. python scripts/05_execute.py 실행 (pytest)",
    "2. python scripts/06_heal.py 실행 (힐링 판단)",
    "3. 실패 시 06a_dialog.py → 힐링 심의 → 패치 → 재실행 (최대 3회)",
    "4. 완료 후 state/pipeline.json step='done'으로 업데이트",
]

print("\n".join(lines))
