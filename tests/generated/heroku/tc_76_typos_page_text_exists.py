from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_typos_page_text_exists(page: Page):
    page.goto("https://the-internet.herokuapp.com/typos")
    page.wait_for_load_state("domcontentloaded")

    expect(page.locator("h3")).to_contain_text("Typos", timeout=10000)

    paragraphs = page.locator("div#content p")
    count = paragraphs.count()
    assert count >= 2, f"Expected at least 2 paragraphs, got {count}"
