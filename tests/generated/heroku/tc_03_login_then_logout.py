"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_03_login_then_logout (tc_03)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
import json
from pathlib import Path

from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_login_then_logout(page):
    """로그인 후 로그아웃"""
    with open(TEST_DATA_PATH) as f:
        test_data = json.load(f)
    valid_user = test_data["heroku"]["valid_user"]

    page.goto(BASE_URL + "login")
    page.locator("#username").fill(valid_user["username"])
    page.locator("#password").fill(valid_user["password"])
    page.locator("button.radius").click()

    expect(page).to_have_url(BASE_URL + "secure")

    page.locator("a.button.secondary").click()

    expect(page).to_have_url(BASE_URL + "login")
    expect(page.locator("#flash-messages")).to_contain_text(
        "You logged out", timeout=10000
    )
