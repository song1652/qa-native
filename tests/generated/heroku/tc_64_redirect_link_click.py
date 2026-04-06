import re
from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_redirect_link_click(page: Page) -> None:
    page.goto("https://the-internet.herokuapp.com/redirector")
    page.wait_for_load_state("domcontentloaded")

    page.locator("a#redirect").click()
    page.wait_for_load_state("domcontentloaded")

    expect(page).to_have_url(re.compile(r"/status_codes"), timeout=10000)
