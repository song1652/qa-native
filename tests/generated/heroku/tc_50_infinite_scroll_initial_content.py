from pathlib import Path
from playwright.sync_api import Page

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = (
    Path(__file__).resolve().parent.parent.parent.parent
    / "config" / "test_data.json"
)


def test_infinite_scroll_initial_content(page: Page) -> None:
    page.goto("https://the-internet.herokuapp.com/infinite_scroll")
    page.wait_for_load_state("domcontentloaded")

    page.wait_for_selector(".jscroll-added", timeout=10000)

    blocks = page.locator(".jscroll-added")
    count = blocks.count()
    assert count >= 1, (
        f"Expected at least 1 initial content block, got {count}"
    )
