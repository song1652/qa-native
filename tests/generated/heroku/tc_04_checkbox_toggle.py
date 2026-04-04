"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: test_checkbox_toggle (tc_04)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_checkbox_toggle(page):
    """체크박스 토글 — 첫 번째 체크, 두 번째 해제 확인"""
    page.goto(BASE_URL + "checkboxes")

    checkboxes = page.locator("#checkboxes input[type='checkbox']")

    checkboxes.nth(0).click()
    checkboxes.nth(1).click()

    expect(checkboxes.nth(0)).to_be_checked()
    expect(checkboxes.nth(1)).not_to_be_checked()
