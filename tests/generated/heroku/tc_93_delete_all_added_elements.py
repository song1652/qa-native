import json
from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_delete_all_added_elements(page: Page):
    """tc_93: 추가된 요소 모두 삭제 - Add 3개 후 Delete 버튼 3개 모두 클릭 → 비어있음 확인"""
    page.goto("https://the-internet.herokuapp.com/add_remove_elements/")
    page.wait_for_load_state("domcontentloaded")

    add_button = page.get_by_role("button", name="Add Element")
    expect(add_button).to_be_visible(timeout=10000)

    for _ in range(3):
        add_button.click()

    delete_buttons = page.locator("button.added-manually")
    expect(delete_buttons).to_have_count(3, timeout=10000)

    for i in range(3):
        page.locator("button.added-manually").first.click()

    expect(page.locator("button.added-manually")).to_have_count(0, timeout=10000)
