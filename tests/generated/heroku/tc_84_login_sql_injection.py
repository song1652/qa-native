"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_84_login_sql_injection (tc_84)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_84_login_sql_injection(page):
    """SQL Injection 로그인 시도"""
    page.goto(BASE_URL + "login")

    # Enter SQL injection strings
    page.locator("#username").fill("' OR 1=1 --")
    page.locator("#password").fill("' OR 1=1 --")
    page.locator("button.radius").click()

    # Login must fail — SQL injection is not exploitable
    expect(page.locator("#flash-messages")).to_contain_text(
        "Your username is invalid!", timeout=10000
    )
