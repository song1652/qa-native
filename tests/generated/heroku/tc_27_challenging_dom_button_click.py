"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_27_challenging_dom_button_click (tc_27)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_27_challenging_dom_button_click(page):
    """Challenging DOM 버튼 클릭"""
    page.goto(BASE_URL + "challenging_dom")
    expect(page.locator("body")).to_be_visible()

    # Buttons are anchor tags with class "button"
    buttons = page.locator("a.button")
    button_count = buttons.count()
    assert button_count >= 3, f"Expected >= 3 buttons, got {button_count}"

    # Click the first button (non-alert one)
    buttons.first.click()
    page.wait_for_load_state("networkidle", timeout=10000)

    # Table should still exist after click
    expect(page.locator("table")).to_be_visible(timeout=10000)
