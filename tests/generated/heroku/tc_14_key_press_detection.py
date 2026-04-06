"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_14_key_press_detection (tc_14)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_key_press_detection(page):
    """키 입력 감지"""
    page.goto(BASE_URL + "key_presses")

    # Per lessons_learned: Enter key triggers form submit so use A key to avoid page reload
    text_input = page.locator("#target")
    text_input.click()
    text_input.press("A")

    expect(page.locator("#result")).to_contain_text("You entered: A", timeout=10000)
