"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_53_jqueryui_submenu_hover (tc_53)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_53_jqueryui_submenu_hover(page):
    """Enabled 호버 시 서브메뉴 표시 확인 (get_by_role 금지)"""
    page.goto("https://the-internet.herokuapp.com/jqueryui/menu")
    page.wait_for_load_state("domcontentloaded")

    # Hover over "Enabled" top-level item (nth(1), nth(0) is "Disabled")
    page.locator("#menu > li.ui-menu-item").nth(1).hover()
    page.wait_for_timeout(500)

    # After hovering "Enabled", "Downloads" submenu should become visible
    downloads_link = page.locator("#menu a", has_text="Downloads")
    expect(downloads_link).to_be_visible(timeout=5000)
