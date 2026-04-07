"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_81_login_empty_fields (tc_81)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_tc_81_login_empty_fields(page):
    """빈 필드로 로그인 시도 시 에러 메시지 확인"""
    page.goto("https://the-internet.herokuapp.com/login")
    page.wait_for_load_state("domcontentloaded")
    page.locator("button.radius").click()
    flash = page.locator("#flash")
    expect(flash).to_be_visible(timeout=5000)
    expect(flash).to_contain_text("Your username is invalid!")
