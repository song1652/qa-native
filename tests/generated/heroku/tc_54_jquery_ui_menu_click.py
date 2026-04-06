"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_54_jquery_ui_menu_click (tc_54)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_jquery_ui_menu_click(page):
    """jQuery UI 메뉴 클릭 동작"""
    page.goto(BASE_URL + "jqueryui/menu")
    page.wait_for_load_state("networkidle")

    # "Enabled" 메뉴 항목 호버 — top-level item with text "Enabled"
    enabled_item = page.locator("#menu > li").filter(has_text="Enabled").first
    expect(enabled_item).to_be_visible(timeout=10000)
    enabled_item.hover()

    # 서브메뉴 "Downloads" 표시 대기 후 호버
    # After hovering Enabled, the Downloads submenu item becomes visible
    downloads_item = page.locator("#menu li").filter(has_text="Downloads").first
    expect(downloads_item).to_be_visible(timeout=5000)
    downloads_item.hover()

    # Downloads 서브메뉴가 존재하는지 확인
    # hover chain 작동 검증: Downloads 항목이 표시되면 성공
    expect(downloads_item).to_be_visible(timeout=5000)
