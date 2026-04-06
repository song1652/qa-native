from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_dynamic_loading_wait(page: Page):
    """Dynamic Loading 요소 대기"""
    page.goto("https://the-internet.herokuapp.com/dynamic_loading/1")
    page.wait_for_load_state("domcontentloaded")

    start_button = page.get_by_role("button", name="Start")
    expect(start_button).to_be_visible(timeout=10000)
    start_button.click()

    finish_element = page.locator("#finish")
    expect(finish_element).to_be_visible(timeout=15000)
    expect(finish_element).to_contain_text("Hello World!", timeout=10000)
