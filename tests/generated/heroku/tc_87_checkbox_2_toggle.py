"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_87_checkbox_2_toggle (tc_87)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_tc_87_checkbox_2_toggle(page):
    """두 번째 체크박스 초기 체크 확인 후 클릭하여 해제 상태 확인"""
    page.goto("https://the-internet.herokuapp.com/checkboxes")
    page.wait_for_load_state("domcontentloaded")

    checkbox2 = page.locator("#checkboxes input").nth(1)
    expect(checkbox2).to_be_checked()

    checkbox2.click()
    expect(checkbox2).not_to_be_checked()
