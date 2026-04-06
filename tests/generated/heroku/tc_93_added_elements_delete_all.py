"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_93_added_elements_delete_all (tc_93)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_93_added_elements_delete_all(page):
    """추가된 요소 모두 삭제"""
    page.goto(BASE_URL + "add_remove_elements/")

    add_btn = page.locator("button", has_text="Add Element")
    expect(add_btn).to_be_visible(timeout=10000)

    # Add 3 elements
    for _ in range(3):
        add_btn.click()

    delete_buttons = page.locator("#elements button.added-manually")
    expect(delete_buttons).to_have_count(3, timeout=10000)

    # Delete all — always click first since DOM shifts
    for _ in range(3):
        delete_buttons.first.click()

    # Verify no Delete buttons remain
    expect(delete_buttons).to_have_count(0, timeout=10000)
