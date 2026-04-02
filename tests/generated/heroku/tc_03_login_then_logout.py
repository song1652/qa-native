"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/login
케이스: test_login_then_logout (tc_03)
"""
import json
import re
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_login_then_logout(page):
    """로그인 후 로그아웃 — 로그아웃 후 /login 복귀 확인"""
    data = json.loads(TEST_DATA_PATH.read_text(encoding="utf-8"))
    user = data["heroku"]["valid_user"]

    page.goto(f"{BASE_URL}/login")
    page.fill("#username", user["username"])
    page.fill("#password", user["password"])
    page.click("button.radius")

    page.wait_for_load_state("domcontentloaded")
    expect(page).to_have_url(re.compile(r"/secure"))

    page.click('a[href="/logout"]')
    page.wait_for_load_state("domcontentloaded")
    expect(page).to_have_url(re.compile(r"/login"))
    expect(page.locator("#flash")).to_contain_text("You logged out of the secure area!")
