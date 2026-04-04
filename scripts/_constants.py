"""파이프라인 종료 코드 상수."""

# 공통
EXIT_SUCCESS = 0          # 정상 완료
EXIT_ERROR = 1            # 일반 오류

# 힐링 (06_heal.py, 99_merge.py)
EXIT_HEAL_NEEDED = 1      # 실패 정보 저장 → Claude Code 패치 필요
EXIT_HEAL_EXCEEDED = 2    # 최대 힐링 횟수 초과

# 승인 (04_approve.py)
EXIT_REJECTED = 2         # 반려 → 코드 재작성
EXIT_AWAITING_APPROVAL = 3  # 대시보드 승인 대기
