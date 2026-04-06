"""Playwright 테스트 — test_droppable_simple (tc_83)"""
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


def test_droppable_simple(page):
    """Droppable simple"""
    page.goto(BASE_URL + "/droppable")
    page.wait_for_load_state("networkidle")
    _remove_ads(page)

    source = page.locator("#simpleDropContainer #draggable")
    target = page.locator("#simpleDropContainer #droppable")
    source.scroll_into_view_if_needed()
    page.wait_for_timeout(300)

    s = source.bounding_box()
    t = target.bounding_box()
    page.mouse.move(s["x"] + s["width"]/2, s["y"] + s["height"]/2)
    page.mouse.down()
    page.mouse.move(t["x"] + t["width"]/2, t["y"] + t["height"]/2, steps=20)
    page.mouse.up()

    expect(target).to_contain_text("Dropped!", timeout=5000)
