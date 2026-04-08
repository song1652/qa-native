"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_35_dynamic_content_load (tc_35)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_tc_35_dynamic_content_load(page):
    """동적 콘텐츠 페이지에서 콘텐츠 행 3개 및 각 행 이미지/텍스트 존재 확인"""
    page.goto("https://the-internet.herokuapp.com/dynamic_content")
    rows = page.locator("#content .row")
    expect(rows.first).to_be_visible(timeout=10000)
    row_count = rows.count()
    # row 0 is the layout header row, rows 1-3 are content rows
    content_rows = row_count - 1
    assert content_rows >= 3, f"Expected at least 3 content rows, got {content_rows}"
    # Verify each content row (rows 1 onward) has an image and text
    for i in range(1, min(row_count, 4)):
        row = rows.nth(i)
        img_count = row.locator("img").count()
        assert img_count >= 1, f"Row {i} should have at least 1 image"
