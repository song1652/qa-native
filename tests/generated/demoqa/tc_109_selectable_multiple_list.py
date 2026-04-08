import re
from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_selectable_multiple_list_items(page: Page) -> None:
    """tc_109: Selectable Multiple List Items — click 3 items and verify all become active."""
    page.goto(f"{BASE_URL}/selectable", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    # Remove ads/overlays
    page.evaluate(
        "document.querySelectorAll('ins.adsbygoogle, iframe[src*=google], iframe[src*=doubleclick]')"
        ".forEach(e => e.remove())"
    )

    # Ensure "List" tab is active (it should be by default)
    list_tab = page.get_by_role("tab", name="List")
    expect(list_tab).to_be_visible(timeout=10000)
    list_tab.click()
    page.wait_for_timeout(300)

    # Get list items inside the active tab pane
    list_items = page.locator("#demo-tabpane-list .list-group-item")
    expect(list_items.first).to_be_visible(timeout=10000)

    # Click first three items
    list_items.nth(0).click()
    page.wait_for_timeout(200)
    list_items.nth(1).click()
    page.wait_for_timeout(200)
    list_items.nth(2).click()
    page.wait_for_timeout(200)

    # Verify all three are active
    expect(list_items.nth(0)).to_have_class(re.compile(r"active"))
    expect(list_items.nth(1)).to_have_class(re.compile(r"active"))
    expect(list_items.nth(2)).to_have_class(re.compile(r"active"))
