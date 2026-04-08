"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_86_checkbox_1_toggle (tc_86)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_tc_86_checkbox_1_toggle(page):
    """첫 번째 체크박스 초기 해제 확인 후 클릭하여 체크 상태 확인"""
    page.goto("https://the-internet.herokuapp.com/checkboxes")
    page.wait_for_load_state("domcontentloaded")

    checkbox1 = page.locator("#checkboxes input").nth(0)
    expect(checkbox1).not_to_be_checked()

    checkbox1.click()
    expect(checkbox1).to_be_checked()
