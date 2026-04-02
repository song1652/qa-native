"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/login
케이스: test_login_failure_invalid_user (tc_02)
"""
import json
import re
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_login_failure_invalid_user(page):
    """잘못된 계정 로그인 실패 — invalid_user로 로그인 시 에러 메시지 확인"""
    data = json.loads(TEST_DATA_PATH.read_text(encoding="utf-8"))
    user = data["heroku"]["invalid_user"]

    page.goto(f"{BASE_URL}/login")
    page.fill("#username", user["username"])
    page.fill("#password", user["password"])
    page.click("button.radius")

    page.wait_for_load_state("domcontentloaded")
    expect(page).to_have_url(re.compile(r"/login"))
    expect(page.locator("#flash")).to_contain_text("Your username is invalid!")
