"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_42_floating_menu_display (tc_42)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_floating_menu_display(page):
    """플로팅 메뉴 표시 확인"""
    page.goto(BASE_URL + "floating_menu")
    page.wait_for_load_state("networkidle")

    # #menu 요소 존재 및 가시성 확인
    menu = page.locator("#menu")
    expect(menu).to_be_visible(timeout=10000)

    # 메뉴 항목 텍스트 확인
    expect(menu).to_contain_text("Home")
    expect(menu).to_contain_text("News")
    expect(menu).to_contain_text("Contact")
    expect(menu).to_contain_text("About")
