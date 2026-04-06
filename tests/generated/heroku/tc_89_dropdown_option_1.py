"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_89_dropdown_option_1 (tc_89)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_89_dropdown_option_1(page):
    """드롭다운 Option 1 선택"""
    page.goto(BASE_URL + "dropdown")

    dropdown = page.locator("#dropdown")
    expect(dropdown).to_be_visible(timeout=10000)

    # Select "Option 1"
    dropdown.select_option(label="Option 1")

    # Verify selected value is "1"
    expect(dropdown).to_have_value("1")
