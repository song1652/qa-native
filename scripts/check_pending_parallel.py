"""
UserPromptSubmit 훅에서 실행됨.
state/parallel.json의 status=ready이면 subagent 실행 요청을
stdout으로 출력해 Claude 컨텍스트에 주입한다.
"""
import json
import sys
from _paths import PARALLEL_STATE, RUN_PARALLEL_LOG

PARALLEL_STATE_PATH = PARALLEL_STATE

if not PARALLEL_STATE_PATH.exists():
    sys.exit(0)

try:
    data = json.loads(PARALLEL_STATE_PATH.read_text(encoding="utf-8"))
except Exception:
    sys.exit(0)

if data.get("status") != "ready":
    sys.exit(0)

total = data.get("total_count", 0)
targets = data.get("targets", [])

# 로그 파일에서 PARALLEL_SUBAGENT_CONTEXTS 추출
log_path = RUN_PARALLEL_LOG
contexts_json = ""
if log_path.exists():
    log_text = log_path.read_text(encoding="utf-8")
    start_marker = "=== PARALLEL_SUBAGENT_CONTEXTS_START ==="
    end_marker = "=== PARALLEL_SUBAGENT_CONTEXTS_END ==="
    start_idx = log_text.find(start_marker)
    end_idx = log_text.find(end_marker)
    if start_idx != -1 and end_idx != -1:
        contexts_json = log_text[start_idx + len(start_marker):end_idx].strip()

lines = [
    f"[병렬 파이프라인 자동 실행] state/parallel.json에 ready 상태가 감지되었습니다. 즉시 subagent를 실행해주세요.",
    f"대상: {total}개 테스트 파일",
    "",
    "대상 목록:",
]
for t in targets:
    lines.append(f"  - [{t.get('group_label', '')}] {t.get('url', '')} → {t.get('output_path', '')}")

if contexts_json:
    lines += [
        "",
        "=== PARALLEL_SUBAGENT_CONTEXTS_START ===",
        contexts_json,
        "=== PARALLEL_SUBAGENT_CONTEXTS_END ===",
    ]

lines += [
    "",
    "진행 방법: CLAUDE.md의 '병렬 파이프라인' 지침을 따라 실행하세요.",
    "1. 위 PARALLEL_SUBAGENT_CONTEXTS의 각 항목을 Agent tool로 동시에 실행",
    "2. 각 subagent는 컨텍스트의 dom_info와 test_cases를 바탕으로 Playwright 테스트 코드 작성 → output_path에 저장",
    "3. 모든 subagent 완료 후 python parallel/99_merge.py 실행",
    "4. 완료 후 state/parallel.json의 status를 'done'으로 변경",
]

print("\n".join(lines))
