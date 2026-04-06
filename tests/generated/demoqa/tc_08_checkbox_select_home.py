from playwright.sync_api import expect
from pathlib import Path

BASE_URL = "https://demoqa.com"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_checkbox_select_home(page):
    page.goto(f"{BASE_URL}/checkbox", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    # Remove ads
    page.evaluate(
        "document.querySelectorAll('ins.adsbygoogle, iframe[src*=google],"
        " iframe[src*=doubleclick]').forEach(e => e.remove())"
    )

    # Click the Home checkbox — use aria-label or find by title text proximity
    home_checkbox = page.locator(".rc-tree-checkbox[aria-label='Select home']")
    if home_checkbox.count() == 0:
        # Fallback: find checkbox near "Home" title
        home_node = page.locator(".rc-tree-treenode", has=page.locator(".rc-tree-title", has_text="Home"))
        home_checkbox = home_node.locator(".rc-tree-checkbox").first

    home_checkbox.click()
    page.wait_for_timeout(1000)

    # Result area should display selected items
    result = page.locator(".check-result")
    if result.count() == 0:
        result = page.locator("#result")

    expect(result).to_be_visible(timeout=10000)
    result_text = result.inner_text().lower()

    # home and key child nodes should be listed in the result
    assert "home" in result_text, f"Expected 'home' in result, got: {result_text}"
    assert "desktop" in result_text or "documents" in result_text or "downloads" in result_text, (
        f"Expected child items in result, got: {result_text}"
    )
