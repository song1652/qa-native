"""
팀 토론 컨텍스트 준비
LLM 없음. 심의 agent에 전달할 컨텍스트를 수집·출력하고 dialog.json 세션을 초기화한다.
"""
import json
import sys
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

PROJECT_ROOT = Path(__file__).parent.parent
DISCUSS_STATE_PATH = PROJECT_ROOT / "discuss_state.json"
DIALOG_PATH = PROJECT_ROOT / "agents" / "dialog.json"


def read_file(path):
    p = Path(path)
    return p.read_text(encoding="utf-8") if p.exists() else ""


def main():
    if not DISCUSS_STATE_PATH.exists():
        print("[오류] discuss_state.json 없음. run_team.py를 먼저 실행하세요.")
        sys.exit(1)

    discuss = json.loads(DISCUSS_STATE_PATH.read_text(encoding="utf-8"))
    topic = discuss.get("topic", "")
    rejection_reason = discuss.get("rejection_reason", "")

    if not topic:
        print("[오류] 토론 주제 없음.")
        sys.exit(1)

    # 컨텍스트 파일 병렬 읽기
    paths = {
        "team_charter":    PROJECT_ROOT / "agents" / "team_charter.md",
        "senior_role":     PROJECT_ROOT / "agents" / "roles" / "senior.md",
        "junior_role":     PROJECT_ROOT / "agents" / "roles" / "junior.md",
        "lessons_learned": PROJECT_ROOT / "agents" / "lessons_learned.md",
        "team_notes":      PROJECT_ROOT / "agents" / "team_notes.md",
    }
    with ThreadPoolExecutor() as ex:
        futures = {k: ex.submit(read_file, v) for k, v in paths.items()}
        ctx = {k: f.result() for k, f in futures.items()}

    # dialog.json 세션 추가
    if DIALOG_PATH.exists():
        dialog = json.loads(DIALOG_PATH.read_text(encoding="utf-8"))
    else:
        dialog = {"pipeline_url": "", "started_at": datetime.now().isoformat(), "sessions": []}

    rejection_count = discuss.get("rejection_count", 0)
    label = f"팀 토론{f' (재토론 {rejection_count}회차)' if rejection_count else ''}"
    dialog["sessions"].append({
        "stage": "team_discussion",
        "stage_label": label,
        "topic": topic,
        "started_at": datetime.now().isoformat(),
        "completed_at": None,
        "status": "in_progress",
        "round": 0,
        "messages": [],
    })
    DIALOG_PATH.write_text(json.dumps(dialog, ensure_ascii=False, indent=2), encoding="utf-8")

    context_payload = {
        "stage": "team_discussion",
        "topic": topic,
        "rejection_reason": rejection_reason,
        "team_charter": ctx["team_charter"],
        "senior_role": ctx["senior_role"],
        "junior_role": ctx["junior_role"],
        "lessons_learned": ctx["lessons_learned"],
        "team_notes": ctx["team_notes"],
    }

    out = sys.stdout.buffer
    out.write(f"[team] 토론 주제: {topic}\n".encode("utf-8"))
    if rejection_reason:
        out.write(f"[team] 재토론 사유: {rejection_reason}\n".encode("utf-8"))
    out.write(b"\n")
    out.write(b"=== DELIBERATION_CONTEXT_START ===\n")
    out.write(json.dumps(context_payload, ensure_ascii=False).encode("utf-8"))
    out.write(b"\n")
    out.write(b"=== DELIBERATION_CONTEXT_END ===\n")
    out.flush()


if __name__ == "__main__":
    main()
