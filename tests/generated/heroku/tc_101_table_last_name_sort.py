"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/tables
케이스: tc_101_table_last_name_sort (tc_101)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
BASE_URL = "https://the-internet.herokuapp.com"


def test_tc_101_table_last_name_sort(page):
    """테이블 Last Name 컬럼 정렬"""
    page.goto(f"{BASE_URL}/tables")
    page.wait_for_load_state("networkidle")

    # Click the Last Name header (first th in table1)
    page.locator("#table1 thead tr th").nth(0).click()
    page.wait_for_timeout(300)

    classes = page.locator("#table1 thead tr th").nth(0).get_attribute("class") or ""
    assert "headerSortDown" in classes, f"Expected headerSortDown class, got: {classes}"
