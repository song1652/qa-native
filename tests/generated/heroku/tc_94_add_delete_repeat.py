import json
from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_add_delete_repeat(page: Page):
    """tc_94: 요소 추가 삭제 반복 - Add 2 → Delete 1 → Add 1 → Delete 버튼 2개 확인"""
    page.goto("https://the-internet.herokuapp.com/add_remove_elements/")
    page.wait_for_load_state("domcontentloaded")

    add_button = page.get_by_role("button", name="Add Element")
    expect(add_button).to_be_visible(timeout=10000)

    add_button.click()
    add_button.click()

    expect(page.locator("button.added-manually")).to_have_count(2, timeout=10000)

    page.locator("button.added-manually").first.click()

    expect(page.locator("button.added-manually")).to_have_count(1, timeout=10000)

    add_button.click()

    expect(page.locator("button.added-manually")).to_have_count(2, timeout=10000)
