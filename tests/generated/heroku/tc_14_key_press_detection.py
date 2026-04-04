"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: test_key_press_detection (tc_14)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_key_press_detection(page):
    """키 입력 감지 — A 키 입력 후 결과 텍스트 확인"""
    page.goto(BASE_URL + "key_presses")

    page.locator("#target").click()
    page.locator("#target").press("a")

    expect(page.locator("#result")).to_contain_text("You entered: A", timeout=5000)
