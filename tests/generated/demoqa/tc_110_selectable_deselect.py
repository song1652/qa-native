import re
from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_selectable_deselect_item(page: Page) -> None:
    """tc_110: Selectable Deselect Item — click item to select, click again to deselect."""
    page.goto(f"{BASE_URL}/selectable", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    # Remove ads/overlays
    page.evaluate(
        "document.querySelectorAll('ins.adsbygoogle, iframe[src*=google], iframe[src*=doubleclick]')"
        ".forEach(e => e.remove())"
    )

    # Ensure "List" tab is active
    list_tab = page.get_by_role("tab", name="List")
    expect(list_tab).to_be_visible(timeout=10000)
    list_tab.click()
    page.wait_for_timeout(300)

    # Get first list item inside the active tab pane
    first_item = page.locator("#demo-tabpane-list .list-group-item").first
    expect(first_item).to_be_visible(timeout=10000)

    # First click — select item
    first_item.click()
    page.wait_for_timeout(200)
    expect(first_item).to_have_class(re.compile(r"active"))

    # Second click — deselect item
    first_item.click()
    page.wait_for_timeout(200)

    # Verify item is no longer active
    item_class = first_item.get_attribute("class") or ""
    assert "active" not in item_class, f"Item should not be active after deselect, but class is: {item_class}"
