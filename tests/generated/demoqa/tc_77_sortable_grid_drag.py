"""Playwright 테스트 — test_sortable_grid_drag (tc_77)"""
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


def test_sortable_grid_drag(page):
    """Sortable grid drag"""
    page.goto(BASE_URL + "/sortable")
    page.wait_for_load_state("domcontentloaded")
    _remove_ads(page)

    page.locator("#demo-tab-grid").click()
    page.wait_for_timeout(500)

    items = page.locator(".create-grid .list-group-item")
    first_text = items.nth(0).inner_text()
    box0 = items.nth(0).bounding_box()
    box2 = items.nth(2).bounding_box()

    page.mouse.move(box0["x"] + box0["width"] / 2, box0["y"] + box0["height"] / 2)
    page.mouse.down()
    page.mouse.move(box2["x"] + box2["width"] / 2, box2["y"] + box2["height"] / 2, steps=20)
    page.mouse.up()
    page.wait_for_timeout(500)

    new_first = items.nth(0).inner_text()
    assert new_first != first_text, "Grid order should change"
