from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_challenging_dom_button_click(page: Page):
    page.goto("https://the-internet.herokuapp.com/challenging_dom")
    page.wait_for_load_state("domcontentloaded")

    buttons = page.locator("div.example .button")
    expect(buttons.first).to_be_visible(timeout=10000)

    button_count = buttons.count()
    assert button_count == 3, f"Expected 3 buttons, found {button_count}"

    buttons.first.click()
    page.wait_for_load_state("domcontentloaded")

    table = page.locator("table")
    expect(table).to_be_visible(timeout=10000)
