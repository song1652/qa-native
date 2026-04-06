"""Playwright 테스트 — test_resizable_box_with_constraint (tc_81)"""
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


def test_resizable_box_with_constraint(page):
    """Resizable box with constraint"""
    page.goto(BASE_URL + "/resizable")
    page.wait_for_load_state("networkidle")
    _remove_ads(page)

    box = page.locator("#resizableBoxWithRestriction")
    handle = box.locator("span.react-resizable-handle")
    handle_box = handle.bounding_box()

    page.mouse.move(handle_box["x"] + 5, handle_box["y"] + 5)
    page.mouse.down()
    page.mouse.move(handle_box["x"] + 200, handle_box["y"] + 100, steps=20)
    page.mouse.up()
    page.wait_for_timeout(300)

    new_box = box.bounding_box()
    assert new_box["width"] > 200, f"Box should be wider, got: {new_box['width']}"
    assert new_box["width"] <= 500, f"Box should respect max constraint"
