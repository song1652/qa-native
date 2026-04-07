"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_02_login_invalid_user (tc_02)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
import json
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_02_login_invalid_user(page):
    """잘못된 계정으로 로그인 시 에러 메시지 표시 확인"""
    data = json.load(open(TEST_DATA_PATH))["heroku"]["invalid_user"]
    page.goto(BASE_URL + "login")
    page.wait_for_load_state("domcontentloaded")
    page.locator("#username").fill(data["username"])
    page.locator("#password").fill(data["password"])
    page.locator("button.radius").click()
    expect(page.locator("#flash")).to_contain_text("Your username is invalid!", timeout=10000)
