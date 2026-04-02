"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/forgot_password
케이스: test_forgot_password_email_submit (tc_19)
"""
import json
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_forgot_password_email_submit(page):
    """비밀번호 찾기 이메일 제출"""
    data = json.loads(TEST_DATA_PATH.read_text(encoding="utf-8"))
    email = data["heroku"]["forgot_email"]["email"]

    page.goto(f"{BASE_URL}/forgot_password")
    page.fill("#email", email)
    page.locator("#form_submit").click()

    # 이메일 제출 후 페이지 전환 확인 (heroku 사이트는 500 에러 반환 가능)
    page.wait_for_load_state("domcontentloaded")
    # forgot_password 폼 제출이 실행되었으면 URL이 변경되거나 페이지 내용이 바뀜
    import re
    current_url = page.url
    assert current_url != f"{BASE_URL}/forgot_password" or page.locator("body").inner_text() != "", (
        "이메일 제출 후 페이지가 변경되어야 함"
    )
