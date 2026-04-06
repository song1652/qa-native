from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_droppable_prevent_propagation_greedy_inner_drop(page: Page) -> None:
    """tc_112: Droppable Prevent Propagation Greedy Inner Drop.

    Drop onto the inner droppable of the 'Greedy' section.
    Expected: inner shows 'Dropped!', outer stays as 'Drop here' (greedy stops bubbling).
    """
    page.goto(f"{BASE_URL}/droppable", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    # Remove footer/ads/overlays that intercept pointer events
    page.evaluate(
        "document.querySelectorAll('ins.adsbygoogle, iframe[src*=google], iframe[src*=doubleclick], footer, #fixedban')"
        ".forEach(e => e.remove())"
    )

    # Click "Prevent Propogation" tab (note: site has typo "Propogation" not "Propagation")
    prevent_tab = page.locator("#droppableExample-tab-preventPropogation")
    expect(prevent_tab).to_be_visible(timeout=10000)
    prevent_tab.click()
    page.wait_for_timeout(500)

    # Scope to active tab pane
    active_pane = page.locator("#droppableExample-tabpane-preventPropogation.show")
    expect(active_pane).to_be_visible(timeout=5000)

    # Locate the draggable element
    drag_me = active_pane.locator("#dragBox")
    expect(drag_me).to_be_visible(timeout=5000)

    # Locate "Greedy" outer and inner droppable
    greedy_outer = active_pane.locator("#greedyDropBox")
    greedy_inner = active_pane.locator("#greedyDropBoxInner")
    expect(greedy_inner).to_be_visible(timeout=5000)

    # Perform drag using JS simulation
    drag_box = drag_me.bounding_box()
    drop_box = greedy_inner.bounding_box()
    assert drag_box is not None and drop_box is not None

    start_x = drag_box["x"] + drag_box["width"] / 2
    start_y = drag_box["y"] + drag_box["height"] / 2
    end_x = drop_box["x"] + drop_box["width"] / 2
    end_y = drop_box["y"] + drop_box["height"] / 2

    page.evaluate(
        """([sx, sy, ex, ey]) => {
            const dragEl = document.getElementById('dragBox');
            const dropEl = document.getElementById('greedyDropBoxInner');
            const steps = 20;
            function dispatchMouse(el, type, x, y) {
                el.dispatchEvent(new MouseEvent(type, {bubbles: true, cancelable: true, clientX: x, clientY: y}));
            }
            dispatchMouse(dragEl, 'mousedown', sx, sy);
            for (let i = 0; i <= steps; i++) {
                const x = sx + (ex - sx) * i / steps;
                const y = sy + (ey - sy) * i / steps;
                dispatchMouse(dragEl, 'mousemove', x, y);
            }
            dispatchMouse(dropEl, 'mouseup', ex, ey);
        }""",
        [start_x, start_y, end_x, end_y]
    )
    page.wait_for_timeout(500)

    # Verify inner greedy drop zone shows "Dropped!"
    expect(greedy_inner).to_contain_text("Dropped!", timeout=5000)

    # Verify outer greedy box header text still contains "Outer droppable" / "Drop Here"
    # Greedy inner stops propagation so outer should NOT show "Dropped!"
    outer_header_p = greedy_outer.locator("p").first
    outer_text = outer_header_p.inner_text()
    assert "Dropped!" not in outer_text, f"Outer greedy should not show 'Dropped!' but got: {outer_text}"
