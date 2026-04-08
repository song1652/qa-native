"""자동 생성된 Playwright 테스트 코드 — URL: https://the-internet.herokuapp.com/login"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/login"


def test_대소문자_구분_테스트(page):
    """대소문자 혼용 username(TomSmith) 입력 시 로그인 실패 검증"""
    page.goto(BASE_URL)
    page.fill("#username", "TomSmith")
    page.fill("#password", "SuperSecretPassword!")
    page.click("button.radius")

    flash = page.locator("#flash")
    expect(flash).to_be_visible()
    expect(flash).to_contain_text("Your username is invalid!")
    expect(page).to_have_url(BASE_URL)
