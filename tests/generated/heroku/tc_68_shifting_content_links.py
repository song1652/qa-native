"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_68_shifting_content_links (tc_68)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_68_shifting_content_links(page):
    """Shifting Content 페이지에서 3개 예제 링크 존재 확인"""
    page.goto("https://the-internet.herokuapp.com/shifting_content")
    page.wait_for_load_state("domcontentloaded")

    expect(page.get_by_role("link", name="Example 1: Menu Element")).to_be_visible(timeout=5000)
    expect(page.get_by_role("link", name="Example 2: An image")).to_be_visible(timeout=5000)
    expect(page.get_by_role("link", name="Example 3: List")).to_be_visible(timeout=5000)
