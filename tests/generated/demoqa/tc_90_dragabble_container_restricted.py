from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"


def test_dragabble_container_restricted(page: Page):
    """tc_90: Dragabble Container Restricted - element stays within container"""
    page.goto(f"{BASE_URL}/dragabble", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    # Remove ads/footer
    page.evaluate("""
        document.querySelectorAll(
            'ins.adsbygoogle, iframe[src*="google"], iframe[src*="doubleclick"], footer, #fixedban, .ad-banner'
        ).forEach(e => e.remove());
    """)

    # Click "Container Restricted" tab
    container_tab = page.locator("#draggableExample-tab-containerRestriction")
    expect(container_tab).to_be_visible(timeout=10000)
    container_tab.click()
    page.wait_for_timeout(500)

    # Scope to active pane
    active_pane = page.locator("#draggableExample-tabpane-containerRestriction.show")
    expect(active_pane).to_be_visible(timeout=5000)

    # Container class is ".containment-wrapper" (not ".draggable-parent")
    container = active_pane.locator(".containment-wrapper").first
    expect(container).to_be_visible(timeout=5000)

    container_box = container.bounding_box()
    assert container_box is not None, "Container bounding box not found"

    # Find draggable element inside the container
    drag_el = container.locator(".draggable").first
    expect(drag_el).to_be_visible(timeout=5000)

    drag_box = drag_el.bounding_box()
    assert drag_box is not None, "Drag element bounding box not found"

    drag_cx = drag_box["x"] + drag_box["width"] / 2
    drag_cy = drag_box["y"] + drag_box["height"] / 2

    # Try to drag far outside container bounds
    out_x = container_box["x"] + container_box["width"] + 500
    out_y = container_box["y"] + container_box["height"] + 500

    page.evaluate(f"""
        (function() {{
            const container = document.querySelector(
                '#draggableExample-tabpane-containerRestriction.show .containment-wrapper'
            );
            const source = container ? container.querySelector('.draggable') : null;
            if (!source) throw new Error('Drag element in container not found');

            function fire(el, type, x, y) {{
                const evt = new MouseEvent(type, {{
                    bubbles: true, cancelable: true, view: window,
                    clientX: x, clientY: y
                }});
                el.dispatchEvent(evt);
            }}
            fire(source, 'mousedown', {drag_cx}, {drag_cy});
            for (let i = 1; i <= 20; i++) {{
                fire(document, 'mousemove',
                    {drag_cx} + ({out_x} - {drag_cx}) * i / 20,
                    {drag_cy} + ({out_y} - {drag_cy}) * i / 20
                );
            }}
            fire(document, 'mouseup', {out_x}, {out_y});
        }})();
    """)
    page.wait_for_timeout(1000)

    # Verify element is still within container bounds
    new_drag_box = drag_el.bounding_box()
    assert new_drag_box is not None, "Element bounding box not found after drag"

    # Refresh container bounds after drag
    new_container_box = container.bounding_box()
    assert new_container_box is not None, "Container bounding box not found after drag"

    # Element left edge should be >= container left edge
    assert new_drag_box["x"] >= new_container_box["x"] - 5, (
        f"Element escaped container on left: el_x={new_drag_box['x']}, container_x={new_container_box['x']}"
    )
    # Element right edge should be <= container right edge
    el_right = new_drag_box["x"] + new_drag_box["width"]
    container_right = new_container_box["x"] + new_container_box["width"]
    assert el_right <= container_right + 5, (
        f"Element escaped container on right: el_right={el_right}, container_right={container_right}"
    )
    # Element top edge should be >= container top edge
    assert new_drag_box["y"] >= new_container_box["y"] - 5, (
        f"Element escaped container on top: el_y={new_drag_box['y']}, container_y={new_container_box['y']}"
    )
    # Element bottom edge should be <= container bottom edge
    el_bottom = new_drag_box["y"] + new_drag_box["height"]
    container_bottom = new_container_box["y"] + new_container_box["height"]
    assert el_bottom <= container_bottom + 5, (
        f"Element escaped container on bottom: el_bottom={el_bottom}, container_bottom={container_bottom}"
    )
