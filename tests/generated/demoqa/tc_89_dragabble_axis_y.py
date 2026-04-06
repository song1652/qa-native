import pytest
from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"


def test_dragabble_axis_y(page: Page):
    """tc_89: Dragabble Axis Y - element moves only along Y axis"""
    page.goto(f"{BASE_URL}/dragabble", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    # Remove ads/footer
    page.evaluate("""
        document.querySelectorAll(
            'ins.adsbygoogle, iframe[src*="google"], iframe[src*="doubleclick"], footer, #fixedban, .ad-banner'
        ).forEach(e => e.remove());
    """)

    # Click "Axis Restricted" tab
    axis_tab = page.locator("#draggableExample-tab-axisRestriction")
    expect(axis_tab).to_be_visible(timeout=10000)
    axis_tab.click()
    page.wait_for_timeout(500)

    # Scope to active pane
    active_pane = page.locator("#draggableExample-tabpane-axisRestriction.show")

    # Find "Only Y" draggable element
    only_y = active_pane.locator("#restrictedY")
    expect(only_y).to_be_visible(timeout=5000)

    # Record initial position
    initial_box = only_y.bounding_box()
    assert initial_box is not None, "Element bounding box not found"

    initial_cx = initial_box["x"] + initial_box["width"] / 2
    initial_cy = initial_box["y"] + initial_box["height"] / 2
    target_x = initial_cx + 100  # Attempt to move in X too
    target_y = initial_cy + 100

    # Perform drag
    page.evaluate(f"""
        (function() {{
            const source = document.querySelector('#draggableExample-tabpane-axisRestriction.show #restrictedY');
            if (!source) throw new Error('Only Y element not found');

            function fire(el, type, x, y) {{
                const evt = new MouseEvent(type, {{
                    bubbles: true, cancelable: true, view: window,
                    clientX: x, clientY: y
                }});
                el.dispatchEvent(evt);
            }}
            fire(source, 'mousedown', {initial_cx}, {initial_cy});
            for (let i = 1; i <= 20; i++) {{
                fire(document, 'mousemove',
                    {initial_cx} + ({target_x} - {initial_cx}) * i / 20,
                    {initial_cy} + ({target_y} - {initial_cy}) * i / 20
                );
            }}
            fire(document, 'mouseup', {target_x}, {target_y});
        }})();
    """)
    page.wait_for_timeout(1000)

    # Verify element moved on Y but not X
    new_box = only_y.bounding_box()
    assert new_box is not None, "Element bounding box not found after drag"

    new_cx = new_box["x"] + new_box["width"] / 2
    new_cy = new_box["y"] + new_box["height"] / 2

    # Y should have changed
    assert abs(new_cy - initial_cy) > 10, (
        f"Element did not move on Y axis: initial_y={initial_cy}, new_y={new_cy}"
    )
    # X should remain the same (within small tolerance)
    x_tolerance = 5
    assert abs(new_cx - initial_cx) < x_tolerance, (
        f"Element moved on X axis unexpectedly: initial_x={initial_cx}, new_x={new_cx}"
    )
