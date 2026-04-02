"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/tables
케이스: test_sortable_data_table (tc_17)
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com"


def test_sortable_data_table(page):
    """정렬 가능한 데이터 테이블 — Last Name 정렬"""
    page.goto(f"{BASE_URL}/tables")

    table = page.locator("#table1")
    expect(table).to_be_visible()

    rows = table.locator("tbody tr")
    assert rows.count() >= 4, f"행이 4개 이상이어야 함, 실제: {rows.count()}"

    # Last Name 헤더의 span 클릭 (정렬 트리거)
    header = table.locator("thead th span", has_text="Last Name")
    header.click()

    # 정렬 반영 대기 — 클릭 후 DOM 업데이트를 기다림
    page.wait_for_timeout(500)

    # 정렬 후 Last Name 컬럼 값 추출
    last_names = []
    for i in range(rows.count()):
        cell_text = rows.nth(i).locator("td").nth(0).inner_text()
        last_names.append(cell_text)

    assert last_names == sorted(last_names), (
        f"알파벳순 정렬이어야 함: {last_names}"
    )
