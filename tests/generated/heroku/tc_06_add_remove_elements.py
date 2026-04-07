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


def test_tc_06_add_remove_elements(page):
    """Add Element 3회 클릭 후 Delete 3개 확인, 1개 삭제 후 2개 남는지 확인"""
    page.goto(BASE_URL + "add_remove_elements/")
    page.wait_for_load_state("domcontentloaded")
    add_btn = page.locator("button[onclick='addElement()']")
    add_btn.click()
    add_btn.click()
    add_btn.click()
    delete_buttons = page.locator("#elements button.added-manually")
    expect(delete_buttons).to_have_count(3, timeout=5000)
    delete_buttons.nth(0).click()
    expect(delete_buttons).to_have_count(2, timeout=5000)
