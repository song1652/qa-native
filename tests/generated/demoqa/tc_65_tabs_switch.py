import json
from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_tabs_switch_content_on_click(page: Page):
    page.goto(f"{BASE_URL}/tabs", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)
    page.evaluate(
        "document.querySelectorAll('ins.adsbygoogle, iframe[src*=google], iframe[src*=doubleclick], #fixedban, footer').forEach(e => e.remove())"
    )

    # Click "Origin" tab
    origin_tab = page.locator("#demo-tab-origin")
    expect(origin_tab).to_be_visible(timeout=10000)
    origin_tab.click()
    page.wait_for_timeout(500)

    # Verify Origin tab content is visible
    origin_content = page.locator("#demo-tabpane-origin")
    expect(origin_content).to_be_visible(timeout=5000)
    origin_text = origin_content.inner_text()
    assert len(origin_text.strip()) > 0, "Expected Origin tab to have content"

    # Click "Use" tab
    use_tab = page.locator("#demo-tab-use")
    expect(use_tab).to_be_visible(timeout=5000)
    use_tab.click()
    page.wait_for_timeout(500)

    # Verify Use tab content is visible
    use_content = page.locator("#demo-tabpane-use")
    expect(use_content).to_be_visible(timeout=5000)
    use_text = use_content.inner_text()
    assert len(use_text.strip()) > 0, "Expected Use tab to have content"

    # Verify the content changed between tabs
    assert origin_text.strip() != use_text.strip(), (
        "Expected Origin and Use tabs to show different content"
    )
