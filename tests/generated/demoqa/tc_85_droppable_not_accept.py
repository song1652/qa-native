import pytest
from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"


def test_droppable_not_accept(page: Page):
    """tc_85: Droppable Not Accept - drag non-acceptable element should keep 'Drop here'"""
    page.goto(f"{BASE_URL}/droppable", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    # Remove ads/footer
    page.evaluate("""
        document.querySelectorAll(
            'ins.adsbygoogle, iframe[src*="google"], iframe[src*="doubleclick"], footer, #fixedban, .ad-banner'
        ).forEach(e => e.remove());
    """)

    # Click "Accept" tab
    accept_tab = page.locator("#droppableExample-tab-accept")
    expect(accept_tab).to_be_visible(timeout=10000)
    accept_tab.click()
    page.wait_for_timeout(500)

    # Scope to active tab pane
    active_pane = page.locator("#droppableExample-tabpane-accept.show")

    # Find "Not Acceptable" drag box by text (no stable ID)
    not_acceptable = active_pane.locator(".drag-box", has_text="Not Acceptable")
    expect(not_acceptable).to_be_visible(timeout=5000)

    # Find drop zone
    drop_box = active_pane.locator(".drop-box")
    expect(drop_box).to_be_visible(timeout=5000)

    # Verify initial text
    expect(drop_box).to_contain_text("Drop here", timeout=5000)

    # Get bounding boxes
    drag_box_rect = not_acceptable.bounding_box()
    drop_box_rect = drop_box.bounding_box()

    assert drag_box_rect is not None, "Drag element bounding box not found"
    assert drop_box_rect is not None, "Drop element bounding box not found"

    drag_x = drag_box_rect["x"] + drag_box_rect["width"] / 2
    drag_y = drag_box_rect["y"] + drag_box_rect["height"] / 2
    drop_x = drop_box_rect["x"] + drop_box_rect["width"] / 2
    drop_y = drop_box_rect["y"] + drop_box_rect["height"] / 2

    # Perform drag using JS mouse events
    page.evaluate(f"""
        (function() {{
            const sourceEls = document.querySelectorAll('#droppableExample-tabpane-accept.show .drag-box');
            let source = null;
            for (const el of sourceEls) {{
                if (el.textContent.trim().includes('Not Acceptable')) {{
                    source = el;
                    break;
                }}
            }}
            const target = document.querySelector('#droppableExample-tabpane-accept.show .drop-box');
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
    page.wait_for_timeout(1000)

    # Drop zone text should remain "Drop here"
    expect(drop_box).to_contain_text("Drop here", timeout=5000)
