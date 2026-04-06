"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_86_checkbox_1_toggle (tc_86)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_86_checkbox_1_toggle(page):
    """체크박스 1 토글"""
    page.goto(BASE_URL + "checkboxes")

    # First checkbox is initially unchecked (DOM cache confirmed)
    checkbox1 = page.locator("#checkboxes input").nth(0)
    expect(checkbox1).not_to_be_checked()

    # Toggle (check it)
    checkbox1.click()
    expect(checkbox1).to_be_checked()
