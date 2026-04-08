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


def test_로그인_후_로그아웃(page):
    """정상 로그인 후 로그아웃 시 로그인 페이지로 리디렉션되고 로그아웃 메시지가 표시되는지 검증"""
    page.goto(BASE_URL)
    page.fill("#username", "tomsmith")
    page.fill("#password", "SuperSecretPassword!")
    page.click("button.radius")

    # 로그인 성공 확인
    expect(page).to_have_url(re.compile(r".*/secure"))

    # 로그아웃 클릭
    page.click("a.button.secondary.radius")

    # 로그아웃 후 검증
    flash = page.locator("#flash")
    expect(flash).to_be_visible()
    expect(flash).to_contain_text("You logged out of the secure area!")

    # 로그인 페이지로 리디렉션 확인
    expect(page).to_have_url(re.compile(r".*/login"))
