"""자동 생성된 Playwright 테스트 코드 — URL: https://the-internet.herokuapp.com/login"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/login"


def test_sql_injection_로그인_차단(page):
    """SQL Injection 입력 시 로그인 차단 및 에러 메시지 표시 검증"""
    page.goto(BASE_URL)
    page.fill("#username", "' OR '1'='1")
    page.fill("#password", "' OR '1'='1")
    page.click("button.radius")

    flash = page.locator("#flash")
    expect(flash).to_be_visible()
    expect(flash).to_contain_text("Your username is invalid!")
    expect(page).to_have_url(BASE_URL)
