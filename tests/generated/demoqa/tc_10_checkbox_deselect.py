from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_deselect_home_checkbox_after_selecting(page: Page) -> None:
    """tc_10: Deselect Home Checkbox After Selecting — select then deselect Home, verify result cleared."""
    page.goto(f"{BASE_URL}/checkbox", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    # Remove ads/overlays
    page.evaluate(
        "document.querySelectorAll('ins.adsbygoogle, iframe[src*=google], iframe[src*=doubleclick]')"
        ".forEach(e => e.remove())"
    )

    # Per lessons_learned: rc-tree structure. Checkbox uses `.rc-tree-checkbox[aria-label='Select Home']`
    home_checkbox = page.locator(".rc-tree-checkbox[aria-label='Select Home']")
    expect(home_checkbox).to_be_visible(timeout=10000)

    # First click — select Home (and all children)
    home_checkbox.click()
    page.wait_for_timeout(300)

    # Verify result is shown
    result_area = page.locator("#result")
    expect(result_area).to_be_visible(timeout=5000)

    # Second click — deselect Home
    home_checkbox.click()
    page.wait_for_timeout(300)

    # Verify result area is no longer visible (or empty)
    expect(result_area).to_be_hidden(timeout=5000)
