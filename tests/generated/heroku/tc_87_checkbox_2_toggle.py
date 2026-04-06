"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_87_checkbox_2_toggle (tc_87)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_87_checkbox_2_toggle(page):
    """체크박스 2 토글"""
    page.goto(BASE_URL + "checkboxes")

    # Second checkbox is initially checked (DOM cache confirmed)
    checkbox2 = page.locator("#checkboxes input").nth(1)
    expect(checkbox2).to_be_checked()

    # Toggle (uncheck it)
    checkbox2.click()
    expect(checkbox2).not_to_be_checked()
