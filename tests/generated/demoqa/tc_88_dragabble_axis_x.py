import pytest
from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"


def test_dragabble_axis_x(page: Page):
    """tc_88: Dragabble Axis X - element moves only along X axis"""
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

    # Find "Only X" draggable element
    only_x = active_pane.locator("#restrictedX")
    expect(only_x).to_be_visible(timeout=5000)

    # Record initial position
    initial_box = only_x.bounding_box()
    assert initial_box is not None, "Element bounding box not found"

    initial_cx = initial_box["x"] + initial_box["width"] / 2
    initial_cy = initial_box["y"] + initial_box["height"] / 2
    target_x = initial_cx + 150
    target_y = initial_cy + 100  # Attempt to move in Y too

    # Perform drag
    page.evaluate(f"""
        (function() {{
            const source = document.querySelector('#draggableExample-tabpane-axisRestriction.show #restrictedX');
            if (!source) throw new Error('Only X element not found');

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

    # Verify element moved on X but not Y
    new_box = only_x.bounding_box()
    assert new_box is not None, "Element bounding box not found after drag"

    new_cx = new_box["x"] + new_box["width"] / 2
    new_cy = new_box["y"] + new_box["height"] / 2

    # X should have changed
    assert abs(new_cx - initial_cx) > 10, (
        f"Element did not move on X axis: initial_x={initial_cx}, new_x={new_cx}"
    )
    # Y should remain the same (within small tolerance)
    y_tolerance = 5
    assert abs(new_cy - initial_cy) < y_tolerance, (
        f"Element moved on Y axis unexpectedly: initial_y={initial_cy}, new_y={new_cy}"
    )
