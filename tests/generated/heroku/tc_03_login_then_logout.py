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


def test_tc_03_login_then_logout(page):
    """정상 로그인 후 로그아웃하여 /login 페이지 복귀 확인"""
    data = json.load(open(TEST_DATA_PATH))["heroku"]["valid_user"]
    page.goto(BASE_URL + "login")
    page.wait_for_load_state("domcontentloaded")
    page.locator("#username").fill(data["username"])
    page.locator("#password").fill(data["password"])
    page.locator("button.radius").click()
    page.wait_for_url("**/secure")
    page.locator("a[href='/logout']").click()
    page.wait_for_url("**/login")
    expect(page.locator("#flash")).to_contain_text("You logged out of the secure area!", timeout=10000)
