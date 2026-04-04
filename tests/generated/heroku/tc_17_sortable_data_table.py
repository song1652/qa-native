"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: test_sortable_data_table (tc_17)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_sortable_data_table(page):
    """정렬 가능한 데이터 테이블 — Last Name 클릭 후 알파벳 정렬 확인"""
    page.goto(BASE_URL + "tables")

    rows = page.locator("#table1 tbody tr")
    expect(rows).to_have_count(4, timeout=5000)

    # 정렬 전 데이터 수집
    before = []
    for i in range(4):
        before.append(rows.nth(i).locator("td:nth-child(1)").inner_text())

    # lessons_learned: th가 아닌 내부 span 클릭
    header = page.locator("#table1 thead th:nth-child(1) span")
    header.click()
    page.wait_for_timeout(500)

    # 정렬 후 Last Name 컬럼 값 추출
    after = []
    for i in range(4):
        after.append(rows.nth(i).locator("td:nth-child(1)").inner_text())

    assert after == sorted(after), (
        f"Expected sorted order, got {after}"
    )
