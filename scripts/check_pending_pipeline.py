"""
UserPromptSubmit 훅에서 실행됨.
state/pipeline.json의 step=init이고 url이 있으면
대시보드에서 run_qa.py가 실행된 것이므로 파이프라인 시작을 Claude에 요청한다.
"""
import sys
from _paths import PIPELINE_STATE
from hook_utils import check_state


def _pipeline_ready(s: dict) -> bool:
    # url이 있어야 대시보드에서 실행한 것 (초기화 상태와 구분)
    if not s.get("url", ""):
        return False
    # dom_info가 이미 있으면 01_analyze 완료된 것 → 중복 방지
    if s.get("dom_info"):
        return False
    return True


state = check_state(PIPELINE_STATE, key="step", value="init", extra_check=_pipeline_ready)
if state is None:
    sys.exit(0)

url = state.get("url", "")
case_count = len(state.get("test_cases", []))

lines = [
    "[파이프라인 자동 실행] 대시보드에서 run_qa.py가 실행되었습니다.",
    f"URL: {url}",
    f"케이스: {case_count}개",
    "",
    "CLAUDE.md 파이프라인의 1번 단계부터 실행해주세요:",
    "1. python scripts/01_analyze.py 실행 (DOM 추출)",
    "2. python scripts/02a_dialog.py 실행 → 심의 Agent → plan 확정",
    "3. python scripts/02_generate.py 실행 → 코드 완성",
    "4. python scripts/03_lint.py 실행 → 03a_dialog.py → 심의 Agent → 코드 리뷰",
    "5. 05_execute.py → 06_heal.py → 힐링 루프",
]

print("\n".join(lines))
