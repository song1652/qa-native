from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = (
    Path(__file__).resolve()
    .parent.parent.parent.parent
    / "config" / "test_data.json"
)


def test_jqueryui_menu_items_display(page: Page):
    """jQuery UI 메뉴 항목 표시 확인"""
    page.goto("https://the-internet.herokuapp.com/jqueryui/menu")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(1000)

    menu = page.locator("#menu")
    expect(menu).to_be_visible(timeout=10000)

    # Top-level menu items (Disabled, Enabled) are always visible
    top_items = page.locator("#menu > li.ui-menu-item")
    assert top_items.count() >= 2, f"Expected at least 2 top-level menu items, got {top_items.count()}"

    # Hover over "Enabled" to reveal sub-items
    enabled_item = page.locator("#menu > li.ui-menu-item").nth(1)
    expect(enabled_item).to_be_visible(timeout=5000)
    enabled_item.hover()
    page.wait_for_timeout(500)

    # "Downloads" and "Back to JQuery UI" sub-items should appear
    downloads = page.locator("#menu a", has_text="Downloads")
    expect(downloads).to_be_visible(timeout=5000)

    back_link = page.locator("#menu a", has_text="Back to JQuery UI")
    expect(back_link).to_be_visible(timeout=5000)
