import pytest
from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"


def test_droppable_revertable(page: Page):
    """tc_86: Droppable Revertable - element reverts after drop"""
    page.goto(f"{BASE_URL}/droppable", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    # Remove ads/footer
    page.evaluate("""
        document.querySelectorAll(
            'ins.adsbygoogle, iframe[src*="google"], iframe[src*="doubleclick"], footer, #fixedban, .ad-banner'
        ).forEach(e => e.remove());
    """)

    # Click "Revert Draggable" tab
    revert_tab = page.locator("#droppableExample-tab-revertable")
    expect(revert_tab).to_be_visible(timeout=10000)
    revert_tab.click()
    page.wait_for_timeout(500)

    # Scope to active tab pane
    active_pane = page.locator("#droppableExample-tabpane-revertable.show")

    # Find "Will Revert" drag element
    will_revert = active_pane.locator("#revertable")
    expect(will_revert).to_be_visible(timeout=5000)

    # Find drop zone
    drop_box = active_pane.locator(".drop-box")
    expect(drop_box).to_be_visible(timeout=5000)

    # Record initial position
    initial_box = will_revert.bounding_box()
    assert initial_box is not None, "Drag element bounding box not found"
    initial_x = initial_box["x"]
    initial_y = initial_box["y"]

    drop_box_rect = drop_box.bounding_box()
    assert drop_box_rect is not None, "Drop element bounding box not found"

    drag_x = initial_box["x"] + initial_box["width"] / 2
    drag_y = initial_box["y"] + initial_box["height"] / 2
    drop_x = drop_box_rect["x"] + drop_box_rect["width"] / 2
    drop_y = drop_box_rect["y"] + drop_box_rect["height"] / 2

    # Perform drag
    page.evaluate(f"""
        (function() {{
            const source = document.querySelector('#droppableExample-tabpane-revertable.show #revertable');
            const target = document.querySelector('#droppableExample-tabpane-revertable.show .drop-box');
            if (!source || !target) throw new Error('Elements not found');

            function fire(el, type, x, y) {{
                const evt = new MouseEvent(type, {{
                    bubbles: true, cancelable: true, view: window,
                    clientX: x, clientY: y
                }});
                el.dispatchEvent(evt);
            }}
            fire(source, 'mousedown', {drag_x}, {drag_y});
            for (let i = 1; i <= 20; i++) {{
                fire(document, 'mousemove',
                    {drag_x} + ({drop_x} - {drag_x}) * i / 20,
                    {drag_y} + ({drop_y} - {drag_y}) * i / 20
                );
            }}
            fire(target, 'mouseup', {drop_x}, {drop_y});
        }})();
    """)

    # Wait for revert animation to complete
    page.wait_for_timeout(2000)

    # Verify element has reverted: bounding box should be close to initial position
    reverted_box = will_revert.bounding_box()
    assert reverted_box is not None, "Reverted element bounding box not found"

    # Allow small tolerance for revert position
    tolerance = 20
    assert abs(reverted_box["x"] - initial_x) < tolerance, (
        f"Element did not revert on X axis: initial={initial_x}, current={reverted_box['x']}"
    )
    assert abs(reverted_box["y"] - initial_y) < tolerance, (
        f"Element did not revert on Y axis: initial={initial_y}, current={reverted_box['y']}"
    )
