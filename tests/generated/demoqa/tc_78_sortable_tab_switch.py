import re
from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"


def test_sortable_tab_switch(page: Page):
    page.goto(f"{BASE_URL}/sortable", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    # Remove ads/footer
    page.evaluate("""
        document.querySelectorAll(
            'ins.adsbygoogle, iframe[src*=google], iframe[src*=doubleclick], footer, #fixedban'
        ).forEach(e => e.remove())
    """)

    # Click List tab and verify vertical list layout
    list_tab = page.locator("#demo-tab-list")
    expect(list_tab).to_be_visible(timeout=10000)
    list_tab.click()
    page.wait_for_timeout(500)

    list_pane = page.locator("#demo-tabpane-list")
    expect(list_pane).to_be_visible(timeout=10000)
    list_items = list_pane.locator(".list-group-item")
    expect(list_items.first).to_be_visible(timeout=10000)
    list_count = list_items.count()
    assert list_count > 0, "List tab should show items"

    # Click Grid tab and verify grid layout
    grid_tab = page.locator("#demo-tab-grid")
    expect(grid_tab).to_be_visible(timeout=10000)
    grid_tab.click()
    page.wait_for_timeout(500)

    grid_pane = page.locator("#demo-tabpane-grid")
    expect(grid_pane).to_be_visible(timeout=10000)
    grid_items = grid_pane.locator(".list-group-item")
    expect(grid_items.first).to_be_visible(timeout=10000)
    grid_count = grid_items.count()
    assert grid_count > 0, "Grid tab should show items"

    # Verify list pane is hidden while grid pane is shown
    expect(list_pane).not_to_be_visible(timeout=5000)
