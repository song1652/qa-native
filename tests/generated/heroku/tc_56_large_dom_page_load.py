from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = (
    Path(__file__).resolve()
    .parent.parent.parent.parent
    / "config" / "test_data.json"
)


def test_large_dom_page_load(page: Page):
    """대규모 DOM 페이지 로드"""
    page.goto("https://the-internet.herokuapp.com/large")
    page.wait_for_load_state("domcontentloaded")

    expect(
        page.get_by_role("heading", name="Large & Deep DOM")
    ).to_be_visible(timeout=10000)

    table = page.locator("table")
    expect(table.first).to_be_visible(timeout=10000)
