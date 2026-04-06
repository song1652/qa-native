"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_94_elements_add_delete_repeat (tc_94)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_94_elements_add_delete_repeat(page):
    """요소 추가 삭제 반복"""
    page.goto(BASE_URL + "add_remove_elements/")

    add_btn = page.locator("button", has_text="Add Element")
    expect(add_btn).to_be_visible(timeout=10000)

    # Add 2 elements
    add_btn.click()
    add_btn.click()

    delete_buttons = page.locator("#elements button.added-manually")
    expect(delete_buttons).to_have_count(2, timeout=10000)

    # Delete 1 element
    delete_buttons.first.click()
    expect(delete_buttons).to_have_count(1, timeout=10000)

    # Add 1 more element
    add_btn.click()
    expect(delete_buttons).to_have_count(2, timeout=10000)
