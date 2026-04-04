"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: test_login_success (tc_01)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
import json
import re
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_login_success(page):
    """정상 로그인 성공 — valid_user로 로그인 후 /secure 이동 확인"""
    with open(TEST_DATA_PATH, encoding="utf-8") as f:
        data = json.load(f)["heroku"]["valid_user"]

    page.goto(BASE_URL + "login")
    page.locator("#username").fill(data["username"])
    page.locator("#password").fill(data["password"])
    page.locator("button.radius").click()

    expect(page).to_have_url(re.compile(r"/secure"), timeout=5000)
    expect(page.locator("#flash")).to_contain_text("You logged into a secure area!", timeout=5000)
