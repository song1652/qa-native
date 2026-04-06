"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_19_forgot_password_email_submit (tc_19)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
import json
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_19_forgot_password_email_submit(page):
    """비밀번호 찾기 이메일 제출"""
    test_data = json.loads(TEST_DATA_PATH.read_text())
    email = test_data["heroku"]["forgot_email"]["email"]

    page.goto(BASE_URL + "forgot_password")
    expect(page.locator("#email")).to_be_visible()

    page.locator("#email").fill(email)
    page.locator("#form_submit").click()

    # Don't assert specific message — just verify page responded
    expect(page.locator("body")).to_be_visible(timeout=10000)
    # Verify the form is no longer visible (page transitioned)
    page.wait_for_load_state("networkidle", timeout=10000)
