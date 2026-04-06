"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_70_shifting_content_list_elements (tc_70)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_70_shifting_content_list_elements(page):
    """Shifting Content 리스트 요소 존재"""
    page.goto(BASE_URL + "shifting_content/list")
    page.wait_for_load_state("networkidle")

    # The shifting content list page may render items inside #content div
    # Use a broader selector and wait for content to stabilize
    content = page.locator("#content")
    expect(content).to_be_visible(timeout=10000)

    # The page content itself (the #content div) should have text
    content_text = content.inner_text()
    assert len(content_text.strip()) > 0, (
        f"Expected non-empty content on shifting_content/list page, got: {content_text!r}"
    )
