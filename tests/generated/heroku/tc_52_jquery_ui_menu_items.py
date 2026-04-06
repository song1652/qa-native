"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_52_jquery_ui_menu_items (tc_52)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_jquery_ui_menu_items(page):
    """jQuery UI 메뉴 항목 표시 확인"""
    page.goto(BASE_URL + "jqueryui/menu")
    page.wait_for_load_state("networkidle")

    # 메뉴 요소 존재 확인 - id="menu"
    menu = page.locator("#menu")
    expect(menu).to_be_visible(timeout=10000)

    # Top-level menu items are visible; submenus (Downloads, PDF etc.) are hidden until hover.
    # Use text-based locators for visible top-level items.
    expect(menu.get_by_text("Disabled")).to_be_visible(timeout=5000)
    expect(menu.get_by_text("Enabled")).to_be_visible(timeout=5000)

    # 메뉴 전체 텍스트 포함 확인 (includes hidden submenu text in DOM)
    expect(menu).to_contain_text("Enabled")
    expect(menu).to_contain_text("Downloads")
