"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_32_disappearing_elements_refresh (tc_32)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_tc_32_disappearing_elements_refresh(page):
    """새로고침 후에도 최소 4개 네비게이션 버튼 유지 확인 (Gallery는 비결정적)"""
    page.goto("https://the-internet.herokuapp.com/disappearing_elements")
    expect(page.locator("ul li").first).to_be_visible(timeout=10000)
    page.reload()
    nav_items = page.locator("ul li")
    expect(nav_items.first).to_be_visible(timeout=10000)
    count = nav_items.count()
    assert count >= 4, f"Expected at least 4 nav items after refresh, got {count}"
