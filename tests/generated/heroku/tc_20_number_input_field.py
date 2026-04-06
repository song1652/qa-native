import json
from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_number_input_field(page: Page):
    page.goto("https://the-internet.herokuapp.com/inputs")
    page.wait_for_load_state("domcontentloaded")

    number_input = page.locator("input[type='number']")
    expect(number_input).to_be_visible(timeout=10000)

    number_input.click()
    number_input.fill("42")

    expect(number_input).to_have_value("42", timeout=5000)

    input_type = page.evaluate("document.querySelector('input[type=\"number\"]').type")
    assert input_type == "number", f"Expected input type 'number', got '{input_type}'"
