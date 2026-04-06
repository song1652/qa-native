"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_58_new_window_open (tc_58)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_58_new_window_open(page):
    """새 창 열기"""
    page.goto(BASE_URL + "windows")

    with page.context.expect_page() as new_page_info:
        page.locator("a", has_text="Click Here").click()

    new_page = new_page_info.value
    new_page.wait_for_load_state("domcontentloaded")

    assert "/windows/new" in new_page.url, (
        f"Expected new tab URL to contain '/windows/new', got: {new_page.url}"
    )
