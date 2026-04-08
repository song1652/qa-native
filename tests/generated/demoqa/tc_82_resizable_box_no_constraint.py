from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"


def test_resizable_box_no_constraint(page: Page):
    page.goto(f"{BASE_URL}/resizable", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    # Remove ads/footer/overlays that intercept pointer events
    page.evaluate("""
        document.querySelectorAll(
            'ins.adsbygoogle, iframe[src*=google], iframe[src*=doubleclick], footer, #fixedban'
        ).forEach(e => e.remove())
    """)

    # Resizable box without restriction
    free_box = page.locator("#resizable")
    expect(free_box).to_be_visible(timeout=10000)

    # Scroll into view
    free_box.scroll_into_view_if_needed()
    page.wait_for_timeout(300)

    # Get initial size
    initial_box = free_box.bounding_box()
    assert initial_box is not None, "Free resizable box should have bounding box"

    # Find resize handle
    handle = page.locator("#resizable .react-resizable-handle")
    expect(handle).to_be_visible(timeout=10000)

    handle_box = handle.bounding_box()
    assert handle_box is not None, "Handle should have bounding box"

    start_x = handle_box["x"] + handle_box["width"] / 2
    start_y = handle_box["y"] + handle_box["height"] / 2

    # Drag handle to resize (increase size)
    page.mouse.move(start_x, start_y)
    page.mouse.down()
    page.wait_for_timeout(100)
    page.mouse.move(start_x + 80, start_y + 60, steps=20)
    page.wait_for_timeout(100)
    page.mouse.up()
    page.wait_for_timeout(500)

    # Verify box size changed
    new_box = free_box.bounding_box()
    assert new_box is not None
    assert (new_box["width"] != initial_box["width"] or new_box["height"] != initial_box["height"]), \
        f"Box size should have changed. Initial: {initial_box['width']}x{initial_box['height']}, " \
        f"New: {new_box['width']}x{new_box['height']}"
