"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_36_dynamic_content_refresh_change (tc_36)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_tc_36_dynamic_content_refresh_change(page):
    """새로고침 후 동적 콘텐츠 변경 가능성 확인 (구조 유지)"""
    page.goto("https://the-internet.herokuapp.com/dynamic_content")
    rows = page.locator("#content .row")
    expect(rows.first).to_be_visible(timeout=10000)
    before_count = rows.count()
    page.reload()
    rows_after = page.locator("#content .row")
    expect(rows_after.first).to_be_visible(timeout=10000)
    after_count = rows_after.count()
    # Structure should be maintained: same number of rows
    assert after_count == before_count, (
        f"Row count changed after refresh: {before_count} -> {after_count}"
    )
    # row 0 is layout header, rows 1-3 are content
    content_rows = after_count - 1
    assert content_rows >= 3, f"Expected at least 3 content rows after refresh, got {content_rows}"
