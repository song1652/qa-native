"""
UserPromptSubmit 훅에서 실행됨.
state/pipeline.json의 step=init이고 url이 있으면
대시보드에서 run_qa.py가 실행된 것이므로 파이프라인 시작을 Claude에 요청한다.
"""
import json
import sys
from _paths import PIPELINE_STATE

STATE_PATH = PIPELINE_STATE

if not STATE_PATH.exists():
    sys.exit(0)

try:
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
except Exception:
    sys.exit(0)

# 대시보드에서 run_qa.py 실행 후 아직 01_analyze 안 된 경우만
if state.get("step") != "init":
    sys.exit(0)

# url이 있어야 대시보드에서 실행한 것 (초기화 상태와 구분)
url = state.get("url", "")
if not url:
    sys.exit(0)

# dom_info가 이미 있으면 01_analyze 완료된 것 → 중복 방지
if state.get("dom_info"):
    sys.exit(0)

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
    "5. python scripts/04_approve.py 실행 → 사용자 승인 대기",
    "6. 승인 시 05_execute.py → 06_heal.py → 힐링 루프",
]

print("\n".join(lines))
