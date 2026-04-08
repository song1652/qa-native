"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_88_checkbox_initial_state (tc_88)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_tc_88_checkbox_initial_state(page):
    """체크박스 2개 존재, 첫 번째 해제/두 번째 체크 초기 상태 확인"""
    page.goto("https://the-internet.herokuapp.com/checkboxes")
    page.wait_for_load_state("domcontentloaded")

    checkboxes = page.locator("#checkboxes input")
    expect(checkboxes).to_have_count(2)

    checkbox1 = checkboxes.nth(0)
    checkbox2 = checkboxes.nth(1)

    expect(checkbox1).not_to_be_checked()
    expect(checkbox2).to_be_checked()
