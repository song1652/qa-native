"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_53_jquery_ui_submenu_hover (tc_53)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_jquery_ui_submenu_hover(page):
    """jQuery UI 서브메뉴 호버 표시"""
    page.goto(BASE_URL + "jqueryui/menu")
    page.wait_for_load_state("networkidle")

    # "Enabled" 항목 호버 - locator().hover() 사용 (lessons: hover 패턴)
    enabled_item = page.locator("#menu li").filter(
        has_text="Enabled"
    ).first
    expect(enabled_item).to_be_visible(timeout=10000)
    enabled_item.hover()

    # 서브메뉴 표시 대기 - "Downloads" 항목이 서브메뉴에 나타남
    downloads_item = page.locator("#menu li").filter(
        has_text="Downloads"
    ).first
    expect(downloads_item).to_be_visible(timeout=5000)
