from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_context_menu_page_content(page: Page) -> None:
    page.goto("https://the-internet.herokuapp.com/context_menu")
    page.wait_for_load_state("domcontentloaded")

    hot_spot = page.locator("#hot-spot")
    expect(hot_spot).to_be_visible(timeout=10000)

    body = page.locator("body")
    expect(body).to_contain_text("right-click", ignore_case=True, timeout=5000)
