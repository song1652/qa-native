from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_redirect_final_url(page: Page) -> None:
    page.goto("https://the-internet.herokuapp.com/redirector")
    page.wait_for_load_state("domcontentloaded")

    page.locator("a#redirect").click()
    page.wait_for_load_state("domcontentloaded")

    expect(page).to_have_url(
        "https://the-internet.herokuapp.com/status_codes", timeout=10000
    )
    expect(page.locator("h3")).to_contain_text("Status Codes", timeout=5000)
