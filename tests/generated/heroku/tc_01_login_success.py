"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_01_login_success (tc_01)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
import json
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_01_login_success(page):
    """유효한 계정으로 로그인 성공 후 /secure 이동 및 플래시 메시지 확인"""
    data = json.load(open(TEST_DATA_PATH))["heroku"]["valid_user"]
    page.goto(BASE_URL + "login")
    page.wait_for_load_state("domcontentloaded")
    page.locator("#username").fill(data["username"])
    page.locator("#password").fill(data["password"])
    page.locator("button.radius").click()
    page.wait_for_url("**/secure")
    expect(page.locator("#flash")).to_contain_text("You logged into a secure area!", timeout=10000)
