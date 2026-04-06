"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_17_sortable_data_table (tc_17)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_17_sortable_data_table(page):
    """정렬 가능한 데이터 테이블"""
    page.goto(BASE_URL + "tables")
    expect(page.locator("#table1")).to_be_visible()

    # Verify table has at least 4 rows (excluding header)
    rows = page.locator("#table1 tbody tr")
    row_count = rows.count()
    assert row_count >= 4, f"Expected >= 4 rows, got {row_count}"

    # Click Last Name column header (th direct click is more reliable than span)
    last_name_th = page.locator("#table1 thead tr th").nth(0)
    last_name_th.click()
    page.wait_for_timeout(300)

    # First click applies headerSortDown
    classes = last_name_th.get_attribute("class") or ""
    assert "headerSortDown" in classes or "headerSortUp" in classes, \
        f"Expected sort class after click, got: {classes}"
