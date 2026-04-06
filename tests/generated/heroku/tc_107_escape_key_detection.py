"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/key_presses
케이스: tc_107_escape_key_detection (tc_107)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com"


def test_tc_107_escape_key_detection(page):
    """Escape 키 입력 감지"""
    page.goto(f"{BASE_URL}/key_presses")
    page.wait_for_load_state("networkidle")

    page.locator("#target").click()
    page.keyboard.press("Escape")

    result = page.locator("#result")
    expect(result).to_contain_text("You entered: ESCAPE", timeout=5000)
