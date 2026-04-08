"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/login
생성 케이스: 1개

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
import re
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/login"


def test_공백만_있는_username으로_로그인_시도(page):
    """username에 공백 문자만 입력하면 에러 메시지가 표시되고 로그인 페이지에 머무는지 검증"""
    page.goto(BASE_URL)
    page.fill("#username", "   ")
    page.fill("#password", "SuperSecretPassword!")
    page.click("button.radius")

    # 에러 메시지 검증 - 공백 username 처리
    flash = page.locator("#flash")
    expect(flash).to_be_visible()
    expect(flash).to_contain_text("Your username is invalid!")

    # URL 검증 - 로그인 페이지 유지
    expect(page).to_have_url(re.compile(r".*/login"))
