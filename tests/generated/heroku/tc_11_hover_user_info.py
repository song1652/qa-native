"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/hovers
케이스: test_hover_user_info (tc_11)
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com"


def test_hover_user_info(page):
    """호버 시 사용자 정보 표시 — 첫 번째 이미지 호버"""
    page.goto(f"{BASE_URL}/hovers")

    figures = page.locator(".figure")
    first_figure = figures.nth(0)

    first_figure.locator("img").hover()

    info = first_figure.locator(".figcaption")
    expect(info).to_contain_text("name: user1")
    expect(info.locator("a")).to_contain_text("View profile")
