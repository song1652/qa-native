"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_04_dropdown_select (tc_04)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

BASE_URL = "https://the-internet.herokuapp.com/"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_04_dropdown_select(page):
    """드롭다운에서 Option 1 선택 후 value=1 확인, Option 2 선택 후 value=2 확인"""
    page.goto("https://the-internet.herokuapp.com/dropdown")

    dropdown = page.locator("#dropdown")
    assert dropdown.is_visible()

    page.select_option("#dropdown", value="1")
    selected = page.eval_on_selector("#dropdown", "el => el.value")
    assert selected == "1", f"Expected '1' but got '{selected}'"

    page.select_option("#dropdown", value="2")
    selected = page.eval_on_selector("#dropdown", "el => el.value")
    assert selected == "2", f"Expected '2' but got '{selected}'"
