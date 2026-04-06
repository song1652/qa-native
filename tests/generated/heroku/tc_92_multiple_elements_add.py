"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_92_multiple_elements_add (tc_92)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_92_multiple_elements_add(page):
    """다중 요소 추가"""
    page.goto(BASE_URL + "add_remove_elements/")

    add_btn = page.locator("button", has_text="Add Element")
    expect(add_btn).to_be_visible(timeout=10000)

    # Click Add Element 3 times (task spec says 3)
    for _ in range(3):
        add_btn.click()

    # Verify 3 Delete buttons exist in #elements
    delete_buttons = page.locator("#elements button.added-manually")
    expect(delete_buttons).to_have_count(3, timeout=10000)
