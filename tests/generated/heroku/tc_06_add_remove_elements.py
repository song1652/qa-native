"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: test_add_remove_elements (tc_06)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_add_remove_elements(page):
    """요소 추가 및 삭제 — Add 3회 후 Delete 3개, Delete 1회 후 2개 확인"""
    page.goto(BASE_URL + "add_remove_elements/")

    add_button = page.locator("button", has_text="Add Element")
    for _ in range(3):
        add_button.click()

    delete_buttons = page.locator(".added-manually")
    expect(delete_buttons).to_have_count(3, timeout=5000)

    delete_buttons.first.click()
    expect(delete_buttons).to_have_count(2, timeout=5000)
