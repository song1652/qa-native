"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_26_challenging_dom_table_data (tc_26)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_tc_26_challenging_dom_table_data(page):
    """Challenging DOM 페이지 테이블 존재 및 데이터 행 확인"""
    page.goto("https://the-internet.herokuapp.com/challenging_dom")
    table = page.locator("table")
    expect(table).to_be_visible(timeout=10000)
    # Verify table has header row
    header = page.locator("table thead tr")
    expect(header).to_be_visible(timeout=5000)
    # Verify table has data rows
    rows = page.locator("table tbody tr")
    row_count = rows.count()
    assert row_count >= 1, f"Expected at least 1 data row, got {row_count}"
