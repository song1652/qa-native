from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"

_DND_SCRIPT = """
(args) => {
    const src = document.querySelector(args[0]);
    const dst = document.querySelector(args[1]);
    const dt = {
        _data: {},
        setData: function(k, v) { this._data[k] = v; },
        getData: function(k) { return this._data[k] || ''; },
        effectAllowed: 'all',
        dropEffect: 'move'
    };
    function fire(el, name) {
        const e = document.createEvent('DragEvent');
        e.initEvent(name, true, true);
        Object.defineProperty(e, 'dataTransfer', { value: dt });
        el.dispatchEvent(e);
    }
    fire(src, 'dragstart');
    fire(dst, 'dragenter');
    fire(dst, 'dragover');
    fire(dst, 'drop');
    fire(src, 'dragend');
}
"""


def test_drag_and_drop_b_to_a(page: Page) -> None:
    page.goto("https://the-internet.herokuapp.com/drag_and_drop")
    page.wait_for_load_state("domcontentloaded")

    col_a = page.locator("#column-a")
    col_b = page.locator("#column-b")
    expect(col_a).to_be_visible(timeout=10000)
    expect(col_b).to_be_visible(timeout=10000)

    page.evaluate(_DND_SCRIPT, ["#column-b", "#column-a"])
    page.wait_for_timeout(500)

    col_a_header = page.locator("#column-a header")
    col_b_header = page.locator("#column-b header")
    expect(col_a_header).to_have_text("B", timeout=5000)
    expect(col_b_header).to_have_text("A", timeout=5000)
