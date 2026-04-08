from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"


def test_resizable_box_with_constraint(page: Page):
    page.goto(f"{BASE_URL}/resizable", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    # Remove ads/footer/overlays that intercept pointer events
    page.evaluate("""
        document.querySelectorAll(
            'ins.adsbygoogle, iframe[src*=google], iframe[src*=doubleclick], footer, #fixedban'
        ).forEach(e => e.remove())
    """)

    # Resizable box with restriction
    constrained_box = page.locator("#resizableBoxWithRestriction")
    expect(constrained_box).to_be_visible(timeout=10000)

    # Get initial size
    initial_box = constrained_box.bounding_box()
    assert initial_box is not None, "Constrained box should have bounding box"

    # Scroll box into view
    constrained_box.scroll_into_view_if_needed()
    page.wait_for_timeout(300)

    # Find resize handle (bottom-right corner)
    handle = page.locator("#resizableBoxWithRestriction .react-resizable-handle")
    expect(handle).to_be_visible(timeout=10000)

    handle_box = handle.bounding_box()
    assert handle_box is not None, "Handle should have bounding box"

    start_x = handle_box["x"] + handle_box["width"] / 2
    start_y = handle_box["y"] + handle_box["height"] / 2

    # Drag handle to make box smaller (try to go below min 150x150)
    # Drag toward top-left by 100px
    page.mouse.move(start_x, start_y)
    page.mouse.down()
    page.wait_for_timeout(100)
    page.mouse.move(start_x - 100, start_y - 100, steps=20)
    page.wait_for_timeout(100)
    page.mouse.up()
    page.wait_for_timeout(500)

    # Verify box size is within constraint (min 150x150)
    new_box = constrained_box.bounding_box()
    assert new_box is not None
    assert new_box["width"] >= 148, f"Width should be >= 150, got {new_box['width']}"
    assert new_box["height"] >= 148, f"Height should be >= 150, got {new_box['height']}"

    # Now try to drag to make larger
    handle_box2 = handle.bounding_box()
    assert handle_box2 is not None
    start_x2 = handle_box2["x"] + handle_box2["width"] / 2
    start_y2 = handle_box2["y"] + handle_box2["height"] / 2

    page.mouse.move(start_x2, start_y2)
    page.mouse.down()
    page.wait_for_timeout(100)
    page.mouse.move(start_x2 + 200, start_y2 + 100, steps=20)
    page.wait_for_timeout(100)
    page.mouse.up()
    page.wait_for_timeout(500)

    # Verify box size is within constraint (max 500x300)
    new_box2 = constrained_box.bounding_box()
    assert new_box2 is not None
    assert new_box2["width"] <= 502, f"Width should be <= 500, got {new_box2['width']}"
    assert new_box2["height"] <= 302, f"Height should be <= 300, got {new_box2['height']}"
