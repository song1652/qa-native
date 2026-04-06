"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_30_context_menu_page_content (tc_30)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_30_context_menu_page_content(page):
    """컨텍스트 메뉴 페이지 콘텐츠 확인"""
    page.goto(BASE_URL + "context_menu")
    expect(page.locator("body")).to_be_visible()

    # Verify hot-spot area exists
    hot_spot = page.locator("#hot-spot")
    expect(hot_spot).to_be_visible(timeout=10000)

    # Verify page has instructional text
    content = page.locator("#content")
    expect(content).to_be_visible()
    content_text = content.inner_text()
    assert len(content_text.strip()) > 0, "Expected page content text to be non-empty"
