"""자동 생성된 Playwright 테스트 코드 — URL: https://the-internet.herokuapp.com/login"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/login"


def test_빈_username으로_로그인_시도(page):
    """빈 username으로 로그인 시 에러 메시지 표시 검증"""
    page.goto(BASE_URL)
    page.fill("#username", "")
    page.fill("#password", "SuperSecretPassword!")
    page.click("button.radius")

    flash = page.locator("#flash")
    expect(flash).to_be_visible()
    expect(flash).to_contain_text("Your username is invalid!")
    expect(page).to_have_url(BASE_URL)
