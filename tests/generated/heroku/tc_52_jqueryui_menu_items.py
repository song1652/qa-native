"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_52_jqueryui_menu_items (tc_52)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_52_jqueryui_menu_items(page):
    """jQuery UI 메뉴 존재 및 Enabled/Downloads/Back to JQuery UI 항목 확인"""
    page.goto("https://the-internet.herokuapp.com/jqueryui/menu")
    page.wait_for_load_state("domcontentloaded")

    menu = page.locator("#menu")
    expect(menu).to_be_visible(timeout=10000)

    # Check top-level menu items are present (some may be hidden until hover)
    enabled_link = page.locator("#menu a", has_text="Enabled")
    expect(enabled_link).to_be_attached(timeout=5000)

    downloads_link = page.locator("#menu a", has_text="Downloads")
    assert downloads_link.count() >= 1

    back_link = page.locator("#menu a", has_text="Back to JQuery UI")
    expect(back_link).to_be_attached(timeout=5000)
