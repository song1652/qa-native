"""자동 생성된 Playwright 테스트 코드 — URL: https://the-internet.herokuapp.com/login"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/login"


def test_잘못된_비밀번호_입력_시_에러_메시지_표시(page):
    """잘못된 비밀번호 입력 시 에러 메시지 표시 및 로그인 페이지 유지 검증"""
    page.goto(BASE_URL)
    page.fill("#username", "tomsmith")
    page.fill("#password", "wrongpassword")
    page.click("button.radius")

    flash = page.locator("#flash")
    expect(flash).to_be_visible()
    expect(flash).to_contain_text("Your password is invalid!")
    expect(page).to_have_url(BASE_URL)
