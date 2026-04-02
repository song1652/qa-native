"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/add_remove_elements/
케이스: test_add_remove_elements (tc_06)
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com"


def test_add_remove_elements(page):
    """요소 추가 및 삭제 — Add Element 3회 후 Delete 1회"""
    page.goto(f"{BASE_URL}/add_remove_elements/")

    add_button = page.locator("button", has_text="Add Element")
    add_button.click()
    add_button.click()
    add_button.click()

    delete_buttons = page.locator("#elements .added-manually")
    expect(delete_buttons).to_have_count(3)

    delete_buttons.first.click()
    expect(delete_buttons).to_have_count(2)
