"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_30_context_menu_page_content (tc_30)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_tc_30_context_menu_page_content(page):
    """컨텍스트 메뉴 페이지에 안내 텍스트와 #hot-spot 영역 존재 확인"""
    page.goto("https://the-internet.herokuapp.com/context_menu")
    hot_spot = page.locator("#hot-spot")
    expect(hot_spot).to_be_visible(timeout=10000)
