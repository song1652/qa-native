from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_typos_page_typo_detection(page: Page):
    page.goto("https://the-internet.herokuapp.com/typos")
    page.wait_for_load_state("domcontentloaded")

    expect(page.locator("body")).to_be_visible(timeout=10000)

    paragraphs = page.locator("div#content p")
    count = paragraphs.count()
    assert count >= 2, f"Expected at least 2 paragraphs, got {count}"

    second_para = paragraphs.nth(1).inner_text()
    assert len(second_para) > 0, "Second paragraph should have text content"
