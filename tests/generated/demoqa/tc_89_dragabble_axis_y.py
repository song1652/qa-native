"""Playwright 테스트 — test_dragabble_axis_y (tc_89)"""
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


def test_dragabble_axis_y(page):
    """Drag restricted to Y axis"""
    page.goto(BASE_URL + "/dragabble")
    page.wait_for_load_state("domcontentloaded")
    _remove_ads(page)

    page.locator("#draggableExample-tab-axisRestriction").click()
    page.wait_for_timeout(500)
    _remove_ads(page)

    el = page.locator("#restrictedY")
    expect(el).to_be_visible(timeout=5000)
    el.scroll_into_view_if_needed()
    page.wait_for_timeout(500)
    _remove_ads(page)

    orig_style = el.evaluate("e => e.style.transform || e.style.top || ''")

    # Use JS-based drag simulation for reliability
    el.evaluate("""e => {
        const rect = e.getBoundingClientRect();
        const cx = rect.left + rect.width / 2;
        const cy = rect.top + rect.height / 2;
        const events = ['mousedown', 'mousemove', 'mousemove', 'mouseup'];
        const coords = [
            {x: cx, y: cy},
            {x: cx, y: cy + 50},
            {x: cx, y: cy + 100},
            {x: cx, y: cy + 100}
        ];
        events.forEach((type, i) => {
            const ev = new MouseEvent(type, {
                bubbles: true, cancelable: true,
                clientX: coords[i].x, clientY: coords[i].y
            });
            e.dispatchEvent(ev);
        });
    }""")
    page.wait_for_timeout(500)

    new_style = el.evaluate("e => e.style.transform || e.style.top || ''")
    assert new_style != orig_style, (
        f"Element should have moved. Before: '{orig_style}', After: '{new_style}'"
    )
