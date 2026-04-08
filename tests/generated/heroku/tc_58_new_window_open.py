"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_58_new_window_open (tc_58)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_58_new_window_open(page):
    """Click Here 링크 클릭 후 새 창/탭 열림 및 URL 확인"""
    page.goto("https://the-internet.herokuapp.com/windows")
    page.wait_for_load_state("domcontentloaded")

    with page.expect_popup() as popup_info:
        page.locator("a[href='/windows/new']").click()

    new_window = popup_info.value
    new_window.wait_for_load_state("domcontentloaded")

    expect(new_window).to_have_url("https://the-internet.herokuapp.com/windows/new", timeout=10000)
