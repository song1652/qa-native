"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_96_user_2_profile_hover (tc_96)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_tc_96_user_2_profile_hover(page):
    """두 번째 사용자 이미지 호버 시 name: user2 및 View profile 링크 표시"""
    page.goto("https://the-internet.herokuapp.com/hovers")
    page.wait_for_load_state("domcontentloaded")

    figure = page.locator("div.figure").nth(1)
    figure.hover()

    caption = figure.locator(".figcaption")
    expect(caption).to_be_visible(timeout=5000)
    expect(caption).to_contain_text("name: user2")

    view_profile = caption.locator("a", has_text="View profile")
    expect(view_profile).to_be_visible()
