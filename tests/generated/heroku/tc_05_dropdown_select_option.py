"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_05_dropdown_select_option (tc_05)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_05_dropdown_select_option(page):
    """드롭다운에서 Option 1, Option 2를 순서대로 선택하고 value 확인"""
    page.goto(BASE_URL + "dropdown")
    page.wait_for_load_state("domcontentloaded")
    dropdown = page.locator("#dropdown")
    dropdown.select_option("1")
    expect(dropdown).to_have_value("1", timeout=5000)
    dropdown.select_option("2")
    expect(dropdown).to_have_value("2", timeout=5000)
