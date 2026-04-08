import pytest
from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"


def test_dragabble_simple(page: Page):
    """tc_87: Dragabble Simple - drag element to new position"""
    page.goto(f"{BASE_URL}/dragabble", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    # Remove ads/footer
    page.evaluate("""
        document.querySelectorAll(
            'ins.adsbygoogle, iframe[src*="google"], iframe[src*="doubleclick"], footer, #fixedban, .ad-banner'
        ).forEach(e => e.remove());
    """)

    # Click "Simple" tab (should be default active, but click to ensure)
    simple_tab = page.locator("#draggableExample-tab-simple")
    expect(simple_tab).to_be_visible(timeout=10000)
    simple_tab.click()
    page.wait_for_timeout(500)

    # Scope to active pane
    active_pane = page.locator("#draggableExample-tabpane-simple.show")

    # Find the draggable element
    drag_me = active_pane.locator("#dragBox")
    expect(drag_me).to_be_visible(timeout=5000)

    # Record initial position
    initial_box = drag_me.bounding_box()
    assert initial_box is not None, "Drag element bounding box not found"

    initial_x = initial_box["x"] + initial_box["width"] / 2
    initial_y = initial_box["y"] + initial_box["height"] / 2
    target_x = initial_x + 150
    target_y = initial_y + 100

    # Perform drag using JS mouse events
    page.evaluate(f"""
        (function() {{
            const source = document.querySelector('#draggableExample-tabpane-simple.show #dragBox');
            if (!source) throw new Error('Drag element not found');

            function fire(el, type, x, y) {{
                const evt = new MouseEvent(type, {{
                    bubbles: true, cancelable: true, view: window,
                    clientX: x, clientY: y
                }});
                el.dispatchEvent(evt);
            }}
            fire(source, 'mousedown', {initial_x}, {initial_y});
            for (let i = 1; i <= 20; i++) {{
                fire(document, 'mousemove',
                    {initial_x} + ({target_x} - {initial_x}) * i / 20,
                    {initial_y} + ({target_y} - {initial_y}) * i / 20
                );
            }}
            fire(document, 'mouseup', {target_x}, {target_y});
        }})();
    """)
    page.wait_for_timeout(1000)

    # Verify element moved - new position should differ from initial
    new_box = drag_me.bounding_box()
    assert new_box is not None, "Element bounding box not found after drag"

    new_center_x = new_box["x"] + new_box["width"] / 2
    new_center_y = new_box["y"] + new_box["height"] / 2

    # Element should have moved significantly
    moved_x = abs(new_center_x - initial_x)
    moved_y = abs(new_center_y - initial_y)
    assert moved_x > 10 or moved_y > 10, (
        f"Element did not move: initial=({initial_x},{initial_y}), new=({new_center_x},{new_center_y})"
    )
