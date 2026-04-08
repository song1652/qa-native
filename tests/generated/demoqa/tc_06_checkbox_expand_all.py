from playwright.sync_api import expect
from pathlib import Path

BASE_URL = "https://demoqa.com"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_checkbox_expand_all(page):
    page.goto(f"{BASE_URL}/checkbox", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    # Remove ads
    page.evaluate(
        "document.querySelectorAll('ins.adsbygoogle, iframe[src*=google],"
        " iframe[src*=doubleclick]').forEach(e => e.remove())"
    )

    # Click the expand all button (button with title="Expand all" or SVG icon button)
    expand_btn = page.locator("button[title='Expand all']")
    if expand_btn.count() > 0:
        expand_btn.first.click()
    else:
        # Fallback: click all closed switchers until none remain
        for _ in range(10):
            closed = page.locator(".rc-tree-switcher_close")
            if closed.count() == 0:
                break
            closed.first.click()
            page.wait_for_timeout(300)

    page.wait_for_timeout(1000)

    # After expanding, child nodes should be visible
    # Home node should be visible
    expect(page.locator(".rc-tree-title", has_text="Home")).to_be_visible(timeout=10000)
    # Desktop node should be visible
    expect(page.locator(".rc-tree-title", has_text="Desktop")).to_be_visible(timeout=10000)
    # Documents node should be visible
    expect(page.locator(".rc-tree-title", has_text="Documents")).to_be_visible(timeout=10000)
    # Downloads node should be visible
    expect(page.locator(".rc-tree-title", has_text="Downloads")).to_be_visible(timeout=10000)
