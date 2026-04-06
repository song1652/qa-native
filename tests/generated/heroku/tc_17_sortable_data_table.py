import re
from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_sortable_data_table(page: Page):
    """정렬 가능한 데이터 테이블"""
    page.goto("https://the-internet.herokuapp.com/tables")
    page.wait_for_load_state("domcontentloaded")

    table1 = page.locator("#table1")
    expect(table1).to_be_visible(timeout=10000)

    rows = table1.locator("tbody tr")
    row_count = rows.count()
    assert row_count >= 4, f"Expected at least 4 rows, got {row_count}"

    # Last Name 헤더 클릭 (th 직접 클릭이 가장 확실)
    last_name_header = table1.locator("th", has_text="Last Name")
    last_name_header.click()
    page.wait_for_timeout(300)

    # 첫 클릭 시 headerSortDown 클래스 적용 확인
    expect(last_name_header).to_have_class(re.compile(r"headerSortDown"), timeout=5000)
