from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = (
    Path(__file__).resolve()
    .parent.parent.parent.parent
    / "config" / "test_data.json"
)


def test_jqueryui_menu_click_action(page: Page):
    """jQuery UI 메뉴 클릭 동작"""
    page.goto("https://the-internet.herokuapp.com/jqueryui/menu")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(1000)

    # Hover "Enabled" to reveal sub-menu
    enabled_item = page.locator("#menu > li.ui-menu-item").nth(1)
    expect(enabled_item).to_be_visible(timeout=10000)
    enabled_item.hover()
    page.wait_for_timeout(500)

    # Hover "Downloads" to reveal download sub-menu
    downloads = page.locator("#menu a", has_text="Downloads")
    expect(downloads).to_be_visible(timeout=5000)
    downloads.hover()
    page.wait_for_timeout(500)

    # Verify the PDF link href points to a download path
    pdf_link = page.locator("#menu a", has_text="PDF")
    expect(pdf_link).to_be_visible(timeout=5000)
    href = pdf_link.get_attribute("href")
    assert href is not None and "download" in href, (
        f"Expected PDF link href to contain 'download', got: {href!r}"
    )
