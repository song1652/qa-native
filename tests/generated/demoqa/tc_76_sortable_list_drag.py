"""Playwright 테스트 — test_sortable_list_drag (tc_76)"""
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


def test_sortable_list_drag(page):
    """Sortable list drag"""
    page.goto(BASE_URL + "/sortable")
    page.wait_for_load_state("networkidle")
    _remove_ads(page)
    page.wait_for_timeout(1000)

    items = page.locator(".vertical-list-container .list-group-item")
    expect(items.first).to_be_visible(timeout=5000)

    first_text = items.nth(0).inner_text()

    # HTML5 drag: use dispatchEvent approach
    page.evaluate("""() => {
        const items = document.querySelectorAll('.vertical-list-container .list-group-item');
        const src = items[0];
        const dst = items[2];
        
        const srcRect = src.getBoundingClientRect();
        const dstRect = dst.getBoundingClientRect();
        
        const dataTransfer = new DataTransfer();
        
        src.dispatchEvent(new DragEvent('dragstart', {
            bubbles: true, dataTransfer, clientX: srcRect.x + srcRect.width/2, clientY: srcRect.y + srcRect.height/2
        }));
        dst.dispatchEvent(new DragEvent('dragover', {
            bubbles: true, dataTransfer, clientX: dstRect.x + dstRect.width/2, clientY: dstRect.y + dstRect.height/2
        }));
        dst.dispatchEvent(new DragEvent('drop', {
            bubbles: true, dataTransfer, clientX: dstRect.x + dstRect.width/2, clientY: dstRect.y + dstRect.height/2
        }));
        src.dispatchEvent(new DragEvent('dragend', { bubbles: true, dataTransfer }));
    }""")
    page.wait_for_timeout(1000)

    new_first = items.nth(0).inner_text()
    # If HTML5 drag didn't work, try mouse-based drag as fallback
    if new_first == first_text:
        box0 = items.nth(0).bounding_box()
        box2 = items.nth(2).bounding_box()
        page.mouse.move(box0["x"] + box0["width"]/2, box0["y"] + box0["height"]/2)
        page.mouse.down()
        page.mouse.move(box2["x"] + box2["width"]/2, box2["y"] + box2["height"]/2 + 15, steps=30)
        page.wait_for_timeout(200)
        page.mouse.up()
        page.wait_for_timeout(500)
        new_first = items.nth(0).inner_text()

    assert new_first != first_text, f"Order should change: was {first_text!r}, still {new_first!r}"
