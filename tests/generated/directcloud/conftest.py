"""
DirectCloud 로그인 쿨다운 fixture.

DirectCloud는 계정당 단일 세션(exclusive session) 정책을 사용한다.
310개 테스트를 순차 실행할 때 연속 로그인 간격이 서버 세션 정리 시간보다
짧으면 race condition이 발생해 `/login?redirect_url=%2F` 패턴으로 실패한다.

이 autouse fixture가 테스트 간 최소 2.5초 쿨다운을 강제한다.
tc_*.py 파일 수정 없이 모든 directcloud 테스트에 자동 적용된다.
"""
import time
import pytest

_last_login_completed: float = 0.0
_LOGIN_MIN_INTERVAL: float = 5.0  # 서버 세션 정리 대기 시간(초)


@pytest.fixture(autouse=True)
def directcloud_login_gap():
    """연속 로그인 간 최소 2.5초 간격을 강제한다."""
    global _last_login_completed
    elapsed = time.time() - _last_login_completed
    if elapsed < _LOGIN_MIN_INTERVAL:
        time.sleep(_LOGIN_MIN_INTERVAL - elapsed)
    yield
    _last_login_completed = time.time()
