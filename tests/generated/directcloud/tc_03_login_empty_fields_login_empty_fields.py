"""
자동 생성된 Playwright 테스트 코드
URL: https://web.directcloud.jp/login
케이스: tc_03_login_empty_fields (tc_03_login_empty_fields)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

BASE_URL = "https://web.directcloud.jp/login"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_03_login_empty_fields(page):
    """빈 필드로 로그인 시도"""
    page.goto(BASE_URL)
    page.click('#new_btn_login')
    page.wait_for_timeout(2000)

    assert "/login" in page.url
    assert page.locator('[name="company_code"]').is_visible()
