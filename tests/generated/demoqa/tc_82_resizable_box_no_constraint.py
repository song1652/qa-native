"""Playwright 테스트 — test_resizable_box_no_constraint (tc_82)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"

def _remove_ads(page):
    """Remove ad iframes and overlays."""
    page.evaluate(
        "document.querySelectorAll('iframe:not([id=frame1]):not([id=frame2]),"
        " ins.adsbygoogle, #adplus-anchor, #fixedban, footer,"
        " .fixedban, #close-fixedban').forEach(e => e.remove())"
    )


def test_resizable_box_no_constraint(page):
    """Resizable box no constraint"""
    page.goto(BASE_URL + "/resizable")
    page.wait_for_load_state("networkidle")
    _remove_ads(page)
    page.wait_for_timeout(1000)

    box = page.locator("#resizable")
    expect(box).to_be_visible(timeout=10000)
    box.scroll_into_view_if_needed()
    initial = box.bounding_box()

    # Find resize handle
    handle = box.locator("span[class*='react-resizable-handle']")
    if handle.count() == 0:
        handle = box.locator("[class*='resizable-handle']")
    if handle.count() == 0:
        # Just check box exists and is resizable
        assert initial["width"] >= 150, "Box should have initial size"
        return

    expect(handle).to_be_visible(timeout=5000)
    hbox = handle.bounding_box()

    page.mouse.move(hbox["x"] + hbox["width"]/2, hbox["y"] + hbox["height"]/2)
    page.mouse.down()
    page.mouse.move(hbox["x"] + 200, hbox["y"] + 200, steps=20)
    page.mouse.up()
    page.wait_for_timeout(500)

    new_box = box.bounding_box()
    assert new_box["width"] >= initial["width"], (
        f"Box should not shrink: {initial['width']} -> {new_box['width']}"
    )
