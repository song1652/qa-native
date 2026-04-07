"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_97_user_3_hover_profile_link (tc_97)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
import re

from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_tc_97_user_3_hover_profile_link(page):
    """세 번째 사용자 호버 후 View profile 클릭, /users/3 이동 확인"""
    page.goto("https://the-internet.herokuapp.com/hovers")
    page.wait_for_load_state("domcontentloaded")

    figure = page.locator("div.figure").nth(2)
    figure.hover()

    caption = figure.locator(".figcaption")
    expect(caption).to_be_visible(timeout=5000)
    expect(caption).to_contain_text("name: user3")

    # Verify href before clicking to avoid navigation issues
    view_profile = caption.locator("a", has_text="View profile")
    expect(view_profile).to_be_visible()
    href = view_profile.get_attribute("href")
    assert href is not None and "/users/3" in href, (
        f"Expected href containing /users/3, got '{href}'"
    )

    view_profile.click()
    page.wait_for_load_state("domcontentloaded")
    expect(page).to_have_url(re.compile(r"/users/3"))
