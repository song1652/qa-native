"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/checkboxes
케이스: test_checkbox_toggle (tc_04)
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com"


def test_checkbox_toggle(page):
    """체크박스 토글 — 첫 번째 체크, 두 번째 해제"""
    page.goto(f"{BASE_URL}/checkboxes")

    checkboxes = page.locator("#checkboxes input[type=checkbox]")
    first = checkboxes.nth(0)
    second = checkboxes.nth(1)

    first.click()
    second.click()

    expect(first).to_be_checked()
    expect(second).not_to_be_checked()
