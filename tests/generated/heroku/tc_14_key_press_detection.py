"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/key_presses
케이스: test_key_press_detection (tc_14)
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com"


def test_key_press_detection(page):
    """키 입력 감지 — A 키 입력 후 결과 확인"""
    page.goto(f"{BASE_URL}/key_presses")

    page.locator("#target").click()
    page.locator("#target").press("a")

    expect(page.locator("#result")).to_contain_text("You entered: A")
