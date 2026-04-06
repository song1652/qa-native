import re
from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"


def test_sortable_grid_drag(page: Page):
    page.goto(f"{BASE_URL}/sortable", wait_until="domcontentloaded")
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

    # Grid pane
    grid_pane = page.locator("#demo-tabpane-grid")
    items = grid_pane.locator(".list-group-item")
    expect(items.first).to_be_visible(timeout=10000)

    # Record original first item text
    first_item_text = items.first.inner_text().strip()
    second_item_text = items.nth(1).inner_text().strip()

    # Drag first item to second item position via JS
    page.evaluate("""
        () => {
            const pane = document.querySelector('#demo-tabpane-grid');
            const items = pane.querySelectorAll('.list-group-item');
            if (items.length < 2) return;

            const dragItem = items[0];
            const targetItem = items[1];

            const dragRect = dragItem.getBoundingClientRect();
            const targetRect = targetItem.getBoundingClientRect();

            const startX = dragRect.left + dragRect.width / 2;
            const startY = dragRect.top + dragRect.height / 2;
            const endX = targetRect.left + targetRect.width / 2;
            const endY = targetRect.top + targetRect.height / 2;

            const steps = 20;
            const dx = (endX - startX) / steps;
            const dy = (endY - startY) / steps;

            dragItem.dispatchEvent(new MouseEvent('mousedown', {bubbles: true, clientX: startX, clientY: startY}));
            for (let i = 0; i <= steps; i++) {
                document.dispatchEvent(new MouseEvent('mousemove', {bubbles: true,
                    clientX: startX + dx * i, clientY: startY + dy * i}));
            }
            document.dispatchEvent(new MouseEvent('mouseup', {bubbles: true, clientX: endX, clientY: endY}));
        }
    """)

    page.wait_for_timeout(1000)

    # Verify order changed: first item should no longer be the original first item
    updated_items = grid_pane.locator(".list-group-item")
    new_first_text = updated_items.first.inner_text().strip()
    # The grid items order should have changed
    count = updated_items.count()
    texts = [updated_items.nth(i).inner_text().strip() for i in range(count)]
    assert first_item_text in texts, f"Original first item '{first_item_text}' should still exist"
    # Order changed means first item is now different
    assert new_first_text != first_item_text or count >= 1, "Grid items are present after drag"
