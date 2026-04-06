"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_26_challenging_dom_table_read (tc_26)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_26_challenging_dom_table_read(page):
    """Challenging DOM 테이블 데이터 읽기"""
    page.goto(BASE_URL + "challenging_dom")
    expect(page.locator("body")).to_be_visible()

    table = page.locator("table")
    expect(table).to_be_visible(timeout=10000)

    # Verify header row exists
    headers = page.locator("table thead tr th")
    header_count = headers.count()
    assert header_count > 0, "Expected table headers, got 0"

    # Verify data rows exist
    rows = page.locator("table tbody tr")
    row_count = rows.count()
    assert row_count > 0, "Expected table rows, got 0"
