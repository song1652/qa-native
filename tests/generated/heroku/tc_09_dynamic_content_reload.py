"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_09_dynamic_content_reload (tc_09)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

BASE_URL = "https://the-internet.herokuapp.com/"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_09_dynamic_content_reload(page):
    """동적 콘텐츠 페이지에 .large-10 텍스트 영역이 3개 존재한다"""
    page.goto("https://the-internet.herokuapp.com/dynamic_content")
    page.wait_for_load_state("networkidle")

    # content rows = rows that contain both an image (.large-2 img) and text (.large-10)
    image_rows = page.locator("#content .row:has(.large-2 img)")
    count = image_rows.count()
    assert count == 3, f"Expected 3 content rows with images, got {count}"

    for i in range(count):
        row = image_rows.nth(i)
        assert row.locator(".large-2 img").count() > 0, f"Row {i+1} missing image"
        assert row.locator(".large-10").inner_text().strip() != "", f"Row {i+1} has empty text"
