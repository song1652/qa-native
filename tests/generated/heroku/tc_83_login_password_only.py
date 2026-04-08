"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_83_login_password_only (tc_83)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
import json
from pathlib import Path

from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_83_login_password_only(page):
    """Password만 입력 후 로그인 시도 시 username 에러 메시지 확인"""
    with open(TEST_DATA_PATH) as f:
        test_data = json.load(f)
    password = test_data["heroku"]["valid_user"]["password"]

    page.goto("https://the-internet.herokuapp.com/login")
    page.wait_for_load_state("domcontentloaded")
    page.locator("#password").fill(password)
    page.locator("button.radius").click()
    flash = page.locator("#flash")
    expect(flash).to_be_visible(timeout=5000)
    expect(flash).to_contain_text("Your username is invalid!")
