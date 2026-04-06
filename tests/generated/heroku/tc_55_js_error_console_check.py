"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_55_js_error_console_check (tc_55)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_55_js_error_console_check(page):
    """JavaScript 에러 페이지 콘솔 에러 확인"""
    errors = []

    page.on("pageerror", lambda exc: errors.append(str(exc)))

    page.goto(BASE_URL + "javascript_error", wait_until="networkidle")

    # Give the page a moment for any JS errors to fire
    page.wait_for_timeout(1000)

    assert len(errors) > 0, "Expected at least one JavaScript error on this page"
