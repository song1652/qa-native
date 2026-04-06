"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/hovers
케이스: tc_97_user_3_hover_profile_link (tc_97)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com"


def test_tc_97_user_3_hover_profile_link(page):
    """유저 3 호버 후 프로필 링크 확인"""
    page.goto(f"{BASE_URL}/hovers")
    page.wait_for_load_state("networkidle")

    figure = page.locator("div.figure").nth(2)
    figure.hover()

    caption = figure.locator(".figcaption")
    expect(caption).to_be_visible(timeout=5000)
    expect(caption).to_contain_text("name: user3")

    link = caption.locator("a")
    expect(link).to_be_visible()
    href = link.get_attribute("href")
    assert href is not None and "users/3" in href, f"Expected href with users/3, got: {href}"
