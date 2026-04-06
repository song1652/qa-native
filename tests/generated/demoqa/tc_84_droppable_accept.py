"""Playwright 테스트 — test_droppable_accept (tc_84)"""
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


def test_droppable_accept(page):
    """Droppable accept - drag acceptable element"""
    page.goto(BASE_URL + "/droppable")
    page.wait_for_load_state("networkidle")
    _remove_ads(page)

    page.locator("#droppableExample-tab-accept").click()
    page.wait_for_timeout(500)
    _remove_ads(page)

    source = page.locator("#acceptable")
    target = page.locator("#acceptDropContainer .drop-box")
    expect(source).to_be_visible(timeout=10000)
    expect(target).to_be_visible(timeout=10000)
    source.scroll_into_view_if_needed()
    page.wait_for_timeout(300)

    s = source.bounding_box()
    t = target.bounding_box()
    page.mouse.move(s["x"]+s["width"]/2, s["y"]+s["height"]/2)
    page.mouse.down()
    page.mouse.move(t["x"]+t["width"]/2, t["y"]+t["height"]/2, steps=30)
    page.wait_for_timeout(200)
    page.mouse.up()
    page.wait_for_timeout(500)

    expect(target).to_contain_text("Dropped!", timeout=5000)
