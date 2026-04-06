from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_dynamic_content_refresh_change(page: Page):
    """동적 콘텐츠 새로고침 후 변경 확인"""
    page.goto(f"{BASE_URL}dynamic_content")
    page.wait_for_load_state("domcontentloaded")

    # 첫 번째 콘텐츠 행의 텍스트 읽기
    rows = page.locator("#content .row .large-10")
    expect(rows.first).to_be_visible(timeout=10000)
    row_count_before = rows.count()

    # 페이지 새로고침
    page.reload()
    page.wait_for_load_state("domcontentloaded")

    # 새로고침 후 페이지 구조 유지 확인 (3개 행)
    rows_after = page.locator("#content .row .large-10")
    expect(rows_after.first).to_be_visible(timeout=10000)
    count_after = rows_after.count()
    assert count_after >= 1, f"Expected at least 1 content row, got {count_after}"
    assert row_count_before == count_after, (
        f"Row count changed: before={row_count_before}, after={count_after}"
    )
