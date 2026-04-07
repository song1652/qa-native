"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_60_new_window_return (tc_60)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_60_new_window_return(page):
    """새 창 열기 후 원래 창으로 복귀하여 Opening a new window 제목 확인"""
    page.goto("https://the-internet.herokuapp.com/windows")
    page.wait_for_load_state("domcontentloaded")

    with page.expect_popup() as popup_info:
        page.locator("a[href='/windows/new']").click()

    new_window = popup_info.value
    new_window.wait_for_load_state("domcontentloaded")
    new_window.close()

    # Back to original page — verify its heading
    heading = page.locator("h3")
    expect(heading).to_be_visible(timeout=10000)
    expect(heading).to_contain_text("Opening a new window", timeout=5000)
