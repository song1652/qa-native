import json
from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_add_multiple_elements(page: Page):
    """tc_92: 다중 요소 추가 - Add Element 버튼 5회 클릭 후 Delete 버튼 5개 확인"""
    page.goto("https://the-internet.herokuapp.com/add_remove_elements/")
    page.wait_for_load_state("domcontentloaded")

    add_button = page.get_by_role("button", name="Add Element")
    expect(add_button).to_be_visible(timeout=10000)

    for _ in range(5):
        add_button.click()

    delete_buttons = page.locator("button.added-manually")
    expect(delete_buttons).to_have_count(5, timeout=10000)
