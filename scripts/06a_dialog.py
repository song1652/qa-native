"""
Step 6a — 힐링 심의 컨텍스트 준비
LLM 없음. 심의 agent에 전달할 컨텍스트를 수집·출력한다.
결과는 state.json에만 저장 (dialog.json은 팀 토론 전용).
모든 파일 읽기를 이 스크립트에서 처리 → agent는 파일 읽기 없이 바로 심의 시작.
"""
import json
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor


def read_file(path):
    p = Path(path)
    return p.read_text(encoding="utf-8") if p.exists() else ""


def main():
    state_path = Path("state.json")

    if not state_path.exists():
        print("[오류] state.json 없음.")
        sys.exit(1)

    state = json.loads(state_path.read_text(encoding="utf-8"))
    heal_context = state.get("heal_context")

    if not heal_context:
        print("[오류] heal_context 없음. 06_heal.py를 먼저 실행하세요.")
        sys.exit(1)

    if state.get("step") != "heal_needed":
        print("[스킵] heal_needed 상태가 아님.")
        sys.exit(0)

    generated_path = state.get("generated_file_path", "tests/generated/test_generated.py")

    # 모든 컨텍스트 파일 병렬 읽기 (프로젝트 루트 기준 절대 경로)
    project_root = Path(__file__).parent.parent
    paths = {
        "team_charter":    project_root / "agents/team_charter.md",
        "senior_role":     project_root / "agents/roles/senior.md",
        "junior_role":     project_root / "agents/roles/junior.md",
        "lessons_learned": project_root / "agents/lessons_learned.md",
        "generated_code":  generated_path,
    }
    with ThreadPoolExecutor() as ex:
        futures = {k: ex.submit(read_file, v) for k, v in paths.items()}
        ctx = {k: f.result() for k, f in futures.items()}

    heal_count = heal_context.get("heal_count", 1)
    context_payload = {
        "stage": "healing",
        "url": state["url"],
        "generated_file_path": generated_path,
        "generated_code": ctx["generated_code"],
        "heal_context": heal_context,
        "dom_info": state.get("dom_info", {}),
        "team_charter": ctx["team_charter"],
        "senior_role": ctx["senior_role"],
        "junior_role": ctx["junior_role"],
        "lessons_learned": ctx["lessons_learned"],
    }

    failures = heal_context.get("failures", [])
    print(f"[06a] 힐링 심의 컨텍스트 준비 완료 ({heal_count}회차)")
    print(f"  실패 케이스: {len(failures)}건")
    for i, f in enumerate(failures[:3], 1):
        print(f"    [{i}] {f.get('test_name', 'unknown')}")
    print()
    print("=== DELIBERATION_CONTEXT_START ===")
    print(json.dumps(context_payload, ensure_ascii=False))
    print("=== DELIBERATION_CONTEXT_END ===")


if __name__ == "__main__":
    main()
