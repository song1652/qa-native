"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_54_jqueryui_menu_click (tc_54)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_54_jqueryui_menu_click(page):
    """Enabled 호버 후 Downloads 서브메뉴 호버, 하위 항목 href 확인 (PDF는 href 검증만)"""
    page.goto("https://the-internet.herokuapp.com/jqueryui/menu")
    page.wait_for_load_state("domcontentloaded")

    # Hover "Enabled" (nth=1, nth(0) is "Disabled") to reveal submenu
    page.locator("#menu > li.ui-menu-item").nth(1).hover()
    page.wait_for_timeout(500)

    # Hover "Downloads" submenu item to reveal sub-submenu
    downloads_link = page.locator("#menu a", has_text="Downloads")
    expect(downloads_link).to_be_visible(timeout=5000)
    downloads_link.hover()
    page.wait_for_timeout(500)

    # Verify sub-submenu items have href attributes — PDF link: verify href only (no click)
    pdf_link = page.locator("#menu a[href$='.pdf']").first
    expect(pdf_link).to_be_attached(timeout=5000)
    href = pdf_link.get_attribute("href")
    assert href is not None and ".pdf" in href

    # Also check other sub-submenu items exist with href
    sub_links = page.locator("#menu li.ui-menu-item a[href]")
    count = sub_links.count()
    assert count >= 1
