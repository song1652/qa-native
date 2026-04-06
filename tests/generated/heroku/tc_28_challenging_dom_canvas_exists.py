from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_challenging_dom_canvas_exists(page: Page) -> None:
    page.goto("https://the-internet.herokuapp.com/challenging_dom")
    page.wait_for_load_state("domcontentloaded")

    canvas = page.locator("canvas")
    expect(canvas).to_be_visible(timeout=10000)

    canvas_id = canvas.get_attribute("id")
    assert canvas_id is not None and canvas_id != "", "canvas element must have an id attribute"
