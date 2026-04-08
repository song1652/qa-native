"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_55_javascript_error_console (tc_55)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_55_javascript_error_console(page):
    """JavaScript 에러 페이지 로드 시 콘솔 에러 발생 확인"""
    page_errors = []

    page.on("pageerror", lambda exc: page_errors.append(str(exc)))

    page.goto("https://the-internet.herokuapp.com/javascript_error")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(1000)

    assert len(page_errors) > 0, "Expected at least one JS error on this page"
