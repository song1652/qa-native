"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_91_dropdown_default_selection (tc_91)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_91_dropdown_default_selection(page):
    """드롭다운 기본 선택값 확인"""
    page.goto(BASE_URL + "dropdown")

    dropdown = page.locator("#dropdown")
    expect(dropdown).to_be_visible(timeout=10000)

    # Default option has no value selected — the placeholder option is disabled
    default_option = page.locator("#dropdown option[disabled]")
    expect(default_option).to_have_text(
        "Please select an option"
    )

    # Verify the dropdown shows the placeholder option (value="")
    expect(dropdown).to_have_value("")
