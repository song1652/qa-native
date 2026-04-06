from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_dynamic_loading_wait(page: Page) -> None:
    page.goto("https://the-internet.herokuapp.com/dynamic_loading/1")
    page.wait_for_load_state("domcontentloaded")

    page.get_by_role("button", name="Start").click()

    loading = page.locator("#loading")
    expect(loading).to_be_visible(timeout=5000)

    expect(loading).to_be_hidden(timeout=15000)

    expect(page.locator("#finish")).to_contain_text("Hello World!", timeout=10000)
