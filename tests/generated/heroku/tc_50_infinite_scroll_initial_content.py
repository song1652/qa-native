"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_50_infinite_scroll_initial_content (tc_50)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_50_infinite_scroll_initial_content(page):
    """무한 스크롤 페이지 초기 콘텐츠 블록 최소 1개 존재 확인"""
    page.goto("https://the-internet.herokuapp.com/infinite_scroll")
    page.wait_for_load_state("domcontentloaded")

    # Wait for initial content to appear
    page.wait_for_selector(".jscroll-added", timeout=15000)

    count = page.locator(".jscroll-added").count()
    assert count >= 1
