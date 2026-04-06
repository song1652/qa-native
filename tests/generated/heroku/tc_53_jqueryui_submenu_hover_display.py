from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = (
    Path(__file__).resolve()
    .parent.parent.parent.parent
    / "config" / "test_data.json"
)


def test_jqueryui_submenu_hover_display(page: Page):
    """jQuery UI 서브메뉴 호버 표시"""
    page.goto("https://the-internet.herokuapp.com/jqueryui/menu")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(1000)

    # Hover over "Enabled" top-level item to reveal sub-menu
    enabled_item = page.locator("#menu > li.ui-menu-item").nth(1)
    expect(enabled_item).to_be_visible(timeout=10000)
    enabled_item.hover()
    page.wait_for_timeout(500)

    # "Downloads" sub-item should be visible after hover
    downloads = page.locator("#menu a", has_text="Downloads")
    expect(downloads).to_be_visible(timeout=5000)

    # Hover over "Downloads" to reveal its sub-menu
    downloads.hover()
    page.wait_for_timeout(500)

    # PDF, CSV, Excel sub-items should be visible
    pdf_link = page.locator("#menu a", has_text="PDF")
    expect(pdf_link).to_be_visible(timeout=5000)
