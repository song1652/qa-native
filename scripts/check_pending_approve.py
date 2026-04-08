"""
UserPromptSubmit 훅에서 실행됨.
state/pipeline.json의 step=reviewed이고 execution_result가 없으면
코드 리뷰가 완료된 것이므로 테스트 실행을 Claude에 요청한다.
(승인 단계 제거 — 심의 완료 후 바로 실행)
"""
import sys
from _paths import PIPELINE_STATE
from hook_utils import check_state

state = check_state(
    PIPELINE_STATE,
    key="step",
    value="reviewed",
    extra_check=lambda s: not s.get("execution_result"),
)
if state is None:
    sys.exit(0)

url = state.get("url", "")
case_count = len(state.get("test_cases", []))

lines = [
    "[파이프라인 자동 실행] 코드 리뷰가 완료되었습니다.",
    f"URL: {url}",
    f"케이스: {case_count}개",
    "",
    "CLAUDE.md 파이프라인의 6번 단계부터 실행해주세요:",
    "1. python scripts/05_execute.py 실행 (pytest)",
    "2. python scripts/06_heal.py 실행 (힐링 판단)",
    "3. 실패 시 06a_dialog.py → 힐링 심의 → 패치 → 재실행 (최대 3회)",
    "4. 완료 후 state/pipeline.json step='done'으로 업데이트",
]

print("\n".join(lines))
