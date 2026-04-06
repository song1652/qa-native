import re
from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_abtest_page_load(page: Page):
    page.goto("https://the-internet.herokuapp.com/abtest")
    page.wait_for_load_state("domcontentloaded")

    heading = page.locator("h3")
    expect(heading).to_be_visible(timeout=10000)

    heading_text = heading.inner_text()
    valid_titles = ["A/B Test Control", "A/B Test Variation 1"]
    assert heading_text in valid_titles, f"Unexpected heading: '{heading_text}'"

    body_text = page.locator("div.example p")
    expect(body_text).to_be_visible(timeout=5000)
