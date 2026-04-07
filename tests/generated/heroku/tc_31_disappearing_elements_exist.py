"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_31_disappearing_elements_exist (tc_31)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_tc_31_disappearing_elements_exist(page):
    """사라지는 요소 페이지에서 네비게이션 버튼 최소 4개 존재 확인"""
    page.goto("https://the-internet.herokuapp.com/disappearing_elements")
    nav_items = page.locator("ul li")
    expect(nav_items.first).to_be_visible(timeout=10000)
    count = nav_items.count()
    assert count >= 4, f"Expected at least 4 nav items, got {count}"
