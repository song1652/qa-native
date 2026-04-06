"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_59_new_window_text_check (tc_59)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_59_new_window_text_check(page):
    """새 창 텍스트 확인"""
    page.goto(BASE_URL + "windows")

    with page.context.expect_page() as new_page_info:
        page.locator("a", has_text="Click Here").click()

    new_page = new_page_info.value
    new_page.wait_for_load_state("domcontentloaded")

    expect(new_page.locator("h3")).to_contain_text("New Window", timeout=10000)
