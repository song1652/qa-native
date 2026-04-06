"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_06_add_remove_elements (tc_06)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_add_remove_elements(page):
    """요소 추가 및 삭제"""
    page.goto(BASE_URL + "add_remove_elements/")

    add_button = page.locator("button", has_text="Add Element")

    # Add 3 elements
    add_button.click()
    add_button.click()
    add_button.click()

    delete_buttons = page.locator("#elements button")
    expect(delete_buttons).to_have_count(3, timeout=10000)

    # Remove 1 element
    delete_buttons.first.click()
    expect(delete_buttons).to_have_count(2, timeout=10000)
