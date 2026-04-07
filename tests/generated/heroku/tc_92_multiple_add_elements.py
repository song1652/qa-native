"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_92_multiple_add_elements (tc_92)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_tc_92_multiple_add_elements(page):
    """Add Element 5회 클릭 후 Delete 버튼 5개 생성 확인"""
    page.goto("https://the-internet.herokuapp.com/add_remove_elements/")
    page.wait_for_load_state("domcontentloaded")

    add_button = page.locator("button", has_text="Add Element")
    for _ in range(5):
        add_button.click()

    delete_buttons = page.locator("#elements button.added-manually")
    expect(delete_buttons).to_have_count(5)
