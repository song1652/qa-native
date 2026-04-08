"""
Step 4 — QA 리드 승인 게이트
LLM 없음. state.json의 review_summary를 출력하고 y/n 입력 대기.
결과를 state.json의 approval_status에 저장.
"""
import json
import sys
from pathlib import Path
from _paths import PIPELINE_STATE, read_state, write_state


def main():
    state_path = PIPELINE_STATE
    if not state_path.exists():
        print("[오류] state/pipeline.json 없음.")
        sys.exit(1)

    state = read_state(state_path)

    print()
    print("=" * 60)
    print("  QA 리드 승인 요청")
    print("=" * 60)
    print(f"  URL   : {state['url']}")
    print(f"  케이스 : {len(state['test_cases'])}개")
    print()

    # Claude Code가 작성한 요약 출력
    summary = state.get("review_summary", "요약 없음")
    print("[ 리뷰 요약 ]")
    print(summary)
    print()

    # lint 결과 출력
    lint = state.get("lint_result", {})
    lint_status = "통과" if lint.get("passed") else f"이슈 {lint.get('issue_count', '?')}건"
    print(f"[ lint ] {lint_status}")
    print()

    # 생성 코드 경로 안내
    file_path = state.get("generated_file_path", "")
    print(f"[ 코드 ] {file_path}")
    print()
    print("=" * 60)

    # --auto 플래그 또는 stdin 불가 시 자동 승인 대기 모드
    auto_mode = "--auto" in sys.argv

    if auto_mode:
        # 대시보드 연동: approval_status를 "pending"으로 설정하고 대시보드에서 승인/반려 대기
        # step은 "reviewed"로 유지해야 대시보드에서 승인 버튼이 표시됨
        state["approval_status"] = "pending"
        state["step"] = "reviewed"
        write_state(state_path, state)
        print()
        print("  [대기] 대시보드에서 승인/반려를 기다립니다.")
        print("  대시보드 URL: http://localhost:8766")
        sys.exit(3)   # exit code 3 = awaiting approval
    else:
        # CLI 모드: stdin에서 입력 대기
        try:
            while True:
                answer = input("  승인하시겠습니까? (y=승인 / n=반려): ").strip().lower()
                if answer in ("y", "yes", "n", "no"):
                    break
                print("  y 또는 n을 입력하세요.")
        except EOFError:
            # stdin 없음 (대시보드 등에서 실행) → pending 상태로 전환
            # step은 "reviewed"로 유지해야 대시보드에서 승인 버튼이 표시됨
            state["approval_status"] = "pending"
            state["step"] = "reviewed"
            write_state(state_path, state)
            print()
            print("  [대기] stdin 없음 — 대시보드에서 승인/반려를 기다립니다.")
            sys.exit(3)

        approved = answer in ("y", "yes")

        if approved:
            state["approval_status"] = "approved"
            state["step"] = "approved"
            print()
            print("  [승인] 테스트를 실행합니다.")
        else:
            try:
                reason = input("  반려 사유를 입력하세요: ").strip()
            except EOFError:
                reason = ""
            state["approval_status"] = "rejected"
            state["rejection_reason"] = reason or "사유 미입력"
            state["rejection_count"] = state.get("rejection_count", 0) + 1
            state["step"] = "rejected"
            print()
            print(f"  [반려] 사유: {state['rejection_reason']}")
            print(f"  반려 횟수: {state['rejection_count']}회")
            if state["rejection_count"] >= 3:
                print("  [경고] 3회 반려. 파이프라인을 종료합니다.")

        write_state(state_path, state)

        if not approved:
            print()
            print("[다음] Claude Code가 반려 사유를 반영해 코드를 재작성합니다.")
            sys.exit(2)   # exit code 2 = rejected (Claude Code가 분기 판단용)


if __name__ == "__main__":
    main()
