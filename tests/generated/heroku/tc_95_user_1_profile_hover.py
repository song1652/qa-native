"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/hovers
케이스: tc_95_user_1_profile_hover (tc_95)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com"


def test_tc_95_user_1_profile_hover(page):
    """유저 1 프로필 호버"""
    page.goto(f"{BASE_URL}/hovers")
    page.wait_for_load_state("networkidle")

    figure = page.locator("div.figure").nth(0)
    figure.hover()

    caption = figure.locator(".figcaption")
    expect(caption).to_be_visible(timeout=5000)
    expect(caption).to_contain_text("name: user1")
    expect(caption.locator("a")).to_be_visible()
    expect(caption.locator("a")).to_contain_text("View profile")
