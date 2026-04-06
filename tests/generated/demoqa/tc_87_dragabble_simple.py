"""Playwright 테스트 — test_dragabble_simple (tc_87)"""
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


def test_dragabble_simple(page):
    """Dragabble simple"""
    page.goto(BASE_URL + "/dragabble")
    page.wait_for_load_state("networkidle")
    _remove_ads(page)

    drag = page.locator("#dragBox")
    expect(drag).to_be_visible(timeout=5000)
    original = drag.bounding_box()

    page.mouse.move(original["x"]+original["width"]/2, original["y"]+original["height"]/2)
    page.mouse.down()
    page.mouse.move(original["x"]+original["width"]/2+100, original["y"]+original["height"]/2+100, steps=20)
    page.mouse.up()
    page.wait_for_timeout(300)

    moved = drag.bounding_box()
    assert moved["x"] != original["x"] or moved["y"] != original["y"], "Should move"
