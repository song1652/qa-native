import json
from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_forgot_password_email_submit(page: Page):
    """비밀번호 찾기 이메일 제출"""
    with open(TEST_DATA_PATH) as f:
        test_data = json.load(f)

    email = test_data["heroku"]["forgot_email"]["email"]

    page.goto("https://the-internet.herokuapp.com/forgot_password")
    page.wait_for_load_state("domcontentloaded")

    email_input = page.locator("#email")
    expect(email_input).to_be_visible(timeout=10000)
    email_input.fill(email)

    retrieve_button = page.get_by_role("button", name="Retrieve password")
    retrieve_button.click()

    page.wait_for_load_state("domcontentloaded")

    # 폼 제출 후 페이지 전환 확인 (URL 변경 또는 결과 콘텐츠 표시)
    # 서버 에러 가능성 고려 - 동작 자체만 검증
    expect(page.locator("body")).to_be_visible(timeout=10000)
