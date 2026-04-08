import re
from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"


def test_selectable_grid_item(page: Page):
    page.goto(f"{BASE_URL}/selectable", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    # Remove ads/footer
    page.evaluate("""
        document.querySelectorAll(
            'ins.adsbygoogle, iframe[src*=google], iframe[src*=doubleclick], footer, #fixedban'
        ).forEach(e => e.remove())
    """)

    # Click Grid tab
    grid_tab = page.locator("#demo-tab-grid")
    expect(grid_tab).to_be_visible(timeout=10000)
    grid_tab.click()
    page.wait_for_timeout(500)

    # Get grid pane
    grid_pane = page.locator("#demo-tabpane-grid")
    expect(grid_pane).to_be_visible(timeout=10000)

    items = grid_pane.locator("li.list-group-item")
    expect(items.first).to_be_visible(timeout=10000)

    # Click the first grid item
    first_item = items.first
    first_item.click()
    page.wait_for_timeout(500)

    # Verify the clicked item has active class
    expect(first_item).to_have_class(re.compile(r"active"), timeout=5000)
