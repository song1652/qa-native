"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_81_login_empty_fields (tc_81)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_81_login_empty_fields(page):
    """로그인 빈 필드 제출"""
    page.goto(BASE_URL + "login")

    # Submit with both fields empty
    page.locator("button.radius").click()

    # Expect error — empty username triggers "Your username is invalid!"
    expect(page.locator("#flash-messages")).to_contain_text(
        "Your username is invalid!",
        timeout=10000,
    )
