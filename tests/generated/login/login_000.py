"""자동 생성된 Playwright 테스트 코드 — URL: https://the-internet.herokuapp.com/login"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/login"


def test_정상_로그인_성공(page):
    """유효한 자격증명으로 로그인 시 /secure 이동 및 성공 메시지 표시 검증"""
    page.goto(BASE_URL)
    page.fill("#username", "tomsmith")
    page.fill("#password", "SuperSecretPassword!")
    page.click("button.radius")

    expect(page).to_have_url("https://the-internet.herokuapp.com/secure")
    flash = page.locator("#flash")
    expect(flash).to_be_visible()
    expect(flash).to_contain_text("You logged into a secure area!")
