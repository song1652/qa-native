"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_04_checkbox_toggle (tc_04)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_checkbox_toggle(page):
    """체크박스 토글"""
    page.goto(BASE_URL + "checkboxes")

    # /checkboxes: checkbox1 is unchecked, checkbox2 is checked initially
    checkbox1 = page.locator("#checkboxes input").nth(0)
    checkbox2 = page.locator("#checkboxes input").nth(1)

    # Verify initial state: checkbox1 unchecked, checkbox2 checked
    expect(checkbox1).not_to_be_checked()
    expect(checkbox2).to_be_checked()

    # Toggle checkbox1 (check it)
    checkbox1.click()
    expect(checkbox1).to_be_checked()

    # Toggle checkbox2 (uncheck it)
    checkbox2.click()
    expect(checkbox2).not_to_be_checked()
