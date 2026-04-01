"""
Step 2a — Plan 심의 컨텍스트 준비
LLM 없음. 심의 agent에 전달할 컨텍스트를 수집·출력한다.
결과는 state.json에만 저장 (dialog.json은 팀 토론 전용).
모든 파일 읽기를 이 스크립트에서 처리 → agent는 파일 읽기 없이 바로 심의 시작.
"""
import json
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from _paths import PIPELINE_STATE


def read_file(path):
    p = Path(path)
    return p.read_text(encoding="utf-8") if p.exists() else ""


def main():
    state_path = PIPELINE_STATE

    if not state_path.exists():
        print("[오류] state/pipeline.json 없음.")
        sys.exit(1)

    state = json.loads(state_path.read_text(encoding="utf-8"))

    if not state.get("dom_info"):
        print("[오류] dom_info 없음. 01_analyze.py를 먼저 실행하세요.")
        sys.exit(1)

    # 모든 컨텍스트 파일 병렬 읽기 (프로젝트 루트 기준 절대 경로)
    project_root = Path(__file__).parent.parent
    paths = {
        "team_charter":    project_root / "agents/team_charter.md",
        "senior_role":     project_root / "agents/roles/senior.md",
        "junior_role":     project_root / "agents/roles/junior.md",
        "lessons_learned": project_root / "agents/lessons_learned.md",
    }
    with ThreadPoolExecutor() as ex:
        futures = {k: ex.submit(read_file, v) for k, v in paths.items()}
        ctx = {k: f.result() for k, f in futures.items()}

    # 심의 agent에 전달할 컨텍스트 출력
    context_payload = {
        "stage": "planning",
        "url": state["url"],
        "dom_info": state["dom_info"],
        "test_cases": state["test_cases"],
        "team_charter": ctx["team_charter"],
        "senior_role": ctx["senior_role"],
        "junior_role": ctx["junior_role"],
        "lessons_learned": ctx["lessons_learned"],
    }

    print("[02a] Plan 심의 컨텍스트 준비 완료")
    print(f"  URL: {state['url']}")
    print(f"  DOM 입력필드: {len(state['dom_info'].get('inputs', []))}개  "
          f"버튼: {len(state['dom_info'].get('buttons', []))}개")
    print(f"  테스트 케이스: {len(state['test_cases'])}개")
    print()
    print("=== DELIBERATION_CONTEXT_START ===")
    print(json.dumps(context_payload, ensure_ascii=False))
    print("=== DELIBERATION_CONTEXT_END ===")


if __name__ == "__main__":
    main()
