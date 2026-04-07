"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_27_challenging_dom_button_click (tc_27)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_tc_27_challenging_dom_button_click(page):
    """Challenging DOM 버튼 3개 존재 확인 및 첫 번째 버튼 클릭 후 페이지 정상 갱신"""
    page.goto("https://the-internet.herokuapp.com/challenging_dom")
    buttons = page.locator("a.button")
    expect(buttons.nth(0)).to_be_visible(timeout=10000)
    button_count = buttons.count()
    assert button_count == 3, f"Expected 3 buttons, got {button_count}"
    # Click first button and verify page still renders
    buttons.nth(0).click()
    expect(page.locator("table")).to_be_visible(timeout=10000)
