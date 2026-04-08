"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_51_infinite_scroll_load_more (tc_51)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_51_infinite_scroll_load_more(page):
    """하단 스크롤 후 추가 콘텐츠 블록 로드 확인"""
    page.goto("https://the-internet.herokuapp.com/infinite_scroll")
    page.wait_for_load_state("domcontentloaded")

    # Wait for initial content
    page.wait_for_selector(".jscroll-added", timeout=15000)
    initial_count = page.locator(".jscroll-added").count()

    # Scroll to bottom to trigger loading more content
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(2000)

    # Scroll again to ensure more content loads
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(2000)

    new_count = page.locator(".jscroll-added").count()
    assert new_count > initial_count
