"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_23_basic_auth_success (tc_23)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_tc_23_basic_auth_success(page):
    """Basic Auth URL로 인증 성공 후 Congratulations 메시지 확인"""
    page.goto("https://admin:admin@the-internet.herokuapp.com/basic_auth")
    body = page.locator("body")
    expect(body).to_be_visible(timeout=10000)
    content = page.locator("div.example")
    expect(content).to_contain_text("Congratulations", timeout=10000)
