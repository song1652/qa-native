"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_59_new_window_text (tc_59)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_59_new_window_text(page):
    """새 창에서 New Window 텍스트 표시 확인"""
    page.goto("https://the-internet.herokuapp.com/windows")
    page.wait_for_load_state("domcontentloaded")

    with page.expect_popup() as popup_info:
        page.locator("a[href='/windows/new']").click()

    new_window = popup_info.value
    new_window.wait_for_load_state("domcontentloaded")

    heading = new_window.locator("h3")
    expect(heading).to_be_visible(timeout=10000)
    expect(heading).to_contain_text("New Window", timeout=5000)
