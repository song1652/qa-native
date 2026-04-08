from playwright.sync_api import expect
from pathlib import Path

BASE_URL = "https://demoqa.com"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_checkbox_collapse_all(page):
    page.goto(f"{BASE_URL}/checkbox", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    # Remove ads
    page.evaluate(
        "document.querySelectorAll('ins.adsbygoogle, iframe[src*=google],"
        " iframe[src*=doubleclick]').forEach(e => e.remove())"
    )

    # First expand all
    expand_btn = page.locator("button[title='Expand all']")
    if expand_btn.count() > 0:
        expand_btn.first.click()
    else:
        for _ in range(10):
            closed = page.locator(".rc-tree-switcher_close")
            if closed.count() == 0:
                break
            closed.first.click()
            page.wait_for_timeout(300)

    page.wait_for_timeout(1000)

    # Now collapse all
    collapse_btn = page.locator("button[title='Collapse all']")
    if collapse_btn.count() > 0:
        collapse_btn.first.click()
    else:
        # Fallback: click all open switchers until none remain
        for _ in range(20):
            opened = page.locator(".rc-tree-switcher_open")
            if opened.count() == 0:
                break
            opened.first.click()
            page.wait_for_timeout(300)

    page.wait_for_timeout(1000)

    # After collapsing, only root Home node should be visible
    # Desktop, Documents, Downloads should be hidden
    expect(page.locator(".rc-tree-title", has_text="Home")).to_be_visible(timeout=10000)
    expect(page.locator(".rc-tree-title", has_text="Desktop")).to_be_hidden(timeout=5000)
    expect(page.locator(".rc-tree-title", has_text="Documents")).to_be_hidden(timeout=5000)
    expect(page.locator(".rc-tree-title", has_text="Downloads")).to_be_hidden(timeout=5000)
