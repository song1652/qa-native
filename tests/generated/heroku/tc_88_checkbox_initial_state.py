"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_88_checkbox_initial_state (tc_88)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_88_checkbox_initial_state(page):
    """체크박스 초기 상태 확인"""
    page.goto(BASE_URL + "checkboxes")

    checkboxes = page.locator("#checkboxes input")

    # Verify 2 checkboxes exist
    expect(checkboxes).to_have_count(2, timeout=10000)

    # First checkbox: unchecked, second: checked (DOM cache confirmed)
    expect(checkboxes.nth(0)).not_to_be_checked()
    expect(checkboxes.nth(1)).to_be_checked()
