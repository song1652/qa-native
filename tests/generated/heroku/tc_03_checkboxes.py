"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_03_checkboxes (tc_03)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

BASE_URL = "https://the-internet.herokuapp.com/"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_03_checkboxes(page):
    """첫 번째 체크박스(초기 unchecked) 클릭 시 checked, 두 번째(초기 checked) 클릭 시 unchecked 전환"""
    page.goto("https://the-internet.herokuapp.com/checkboxes")

    checkboxes = page.locator("#checkboxes input[type='checkbox']")
    cb1 = checkboxes.nth(0)
    cb2 = checkboxes.nth(1)

    assert not cb1.is_checked(), "checkbox 1 should be unchecked initially"
    assert cb2.is_checked(), "checkbox 2 should be checked initially"

    cb1.click()
    cb2.click()

    assert cb1.is_checked(), "checkbox 1 should be checked after click"
    assert not cb2.is_checked(), "checkbox 2 should be unchecked after click"
