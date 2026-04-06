"""Playwright 테스트 — test_dragabble_container_restricted (tc_90)"""
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


def test_dragabble_container_restricted(page):
    """Dragabble container restricted"""
    page.goto(BASE_URL + "/dragabble")
    page.wait_for_load_state("networkidle")
    _remove_ads(page)

    page.locator("#draggableExample-tab-containerRestriction").click()
    page.wait_for_timeout(500)

    container = page.locator("#containmentWrapper")
    drag = container.locator(".draggable")
    expect(drag).to_be_visible(timeout=5000)

    container_box = container.bounding_box()
    drag_box = drag.bounding_box()

    # Try to drag far beyond container
    page.mouse.move(drag_box["x"]+drag_box["width"]/2, drag_box["y"]+drag_box["height"]/2)
    page.mouse.down()
    page.mouse.move(container_box["x"]+container_box["width"]+200, container_box["y"]+container_box["height"]+200, steps=20)
    page.mouse.up()
    page.wait_for_timeout(300)

    new_box = drag.bounding_box()
    # Should stay within container bounds
    assert new_box["x"] + new_box["width"] <= container_box["x"] + container_box["width"] + 5
