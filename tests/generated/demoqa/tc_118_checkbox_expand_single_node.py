from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"
TEST_DATA_PATH = (
    Path(__file__).resolve().parent.parent.parent.parent
    / "config" / "test_data.json"
)


def test_checkbox_expand_single_node(page: Page):
    page.goto(f"{BASE_URL}/checkbox")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(2000)

    # Remove ads/overlays
    page.evaluate(
        "document.querySelectorAll("
        "'ins.adsbygoogle, iframe[src*=google],"
        " iframe[src*=doubleclick], #fixedban, footer'"
        ").forEach(e => e.remove())"
    )

    # Click Home node switcher to expand one level only
    home_switcher = page.locator(".rc-tree-switcher_close").first
    expect(home_switcher).to_be_visible(timeout=5000)
    home_switcher.click()
    page.wait_for_timeout(500)

    # Verify Desktop, Documents, Downloads nodes are visible
    expect(
        page.locator(".rc-tree-title").filter(has_text="Desktop")
    ).to_be_visible(timeout=5000)
    expect(
        page.locator(".rc-tree-title").filter(has_text="Documents")
    ).to_be_visible(timeout=5000)
    expect(
        page.locator(".rc-tree-title").filter(has_text="Downloads")
    ).to_be_visible(timeout=5000)

    # Verify Desktop children are not expanded (Notes not visible)
    expect(
        page.locator(".rc-tree-title").filter(has_text="Notes")
    ).to_be_hidden(timeout=3000)
