from playwright.sync_api import expect
from pathlib import Path

BASE_URL = "https://demoqa.com"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"

AD_REMOVE_JS = (
    "document.querySelectorAll("
    "'ins.adsbygoogle, iframe[src*=google], iframe[src*=doubleclick]'"
    ").forEach(e => e.remove())"
)


def test_checkbox_select_single_leaf(page):
    page.goto(f"{BASE_URL}/checkbox", wait_until="domcontentloaded")
    page.evaluate(AD_REMOVE_JS)
    page.wait_for_timeout(2000)

    # Expand all nodes by clicking all closed switchers until none remain
    for _ in range(10):
        closed_switchers = page.locator(".rc-tree-switcher_close")
        count = closed_switchers.count()
        if count == 0:
            break
        closed_switchers.first.click()
        page.wait_for_timeout(300)

    # Click only the "Notes" checkbox
    notes_checkbox = page.locator(".rc-tree-checkbox[aria-label='Select Notes']")
    expect(notes_checkbox).to_be_visible(timeout=10000)
    notes_checkbox.click()
    page.wait_for_timeout(500)

    # Verify result area shows "notes" text only
    result = page.locator("#result")
    expect(result).to_be_visible(timeout=5000)
    expect(result).to_contain_text("notes", timeout=5000)

    # Verify other items are not listed (check that "home" and "desktop" are not in result)
    result_text = result.inner_text().lower()
    assert "home" not in result_text, "Unexpected 'home' found in result"
    assert "desktop" not in result_text, "Unexpected 'desktop' found in result"
