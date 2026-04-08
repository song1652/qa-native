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


def test_tc_04_checkbox_toggle(page):
    """첫 번째 체크박스 체크, 두 번째 해제 후 상태 확인"""
    page.goto(BASE_URL + "checkboxes")
    page.wait_for_load_state("domcontentloaded")
    checkbox1 = page.locator("#checkboxes input").nth(0)
    checkbox2 = page.locator("#checkboxes input").nth(1)
    # checkbox1 is initially unchecked, click to check
    checkbox1.click()
    # checkbox2 is initially checked, click to uncheck
    checkbox2.click()
    expect(checkbox1).to_be_checked(timeout=5000)
    expect(checkbox2).not_to_be_checked(timeout=5000)
