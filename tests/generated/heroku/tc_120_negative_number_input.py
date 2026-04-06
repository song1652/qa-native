from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_negative_number_input(page: Page):
    """숫자 입력 필드에 음수 입력"""
    page.goto("https://the-internet.herokuapp.com/inputs")
    page.wait_for_load_state("domcontentloaded")

    number_input = page.locator("input[type='number']")
    expect(number_input).to_be_visible(timeout=10000)

    number_input.click()
    number_input.fill("-100")

    expect(number_input).to_have_value("-100", timeout=5000)
