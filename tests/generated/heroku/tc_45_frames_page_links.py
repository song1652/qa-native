"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_45_frames_page_links (tc_45)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_45_frames_page_links(page):
    """Frames 페이지에서 Nested Frames와 iFrame 링크 존재 확인"""
    page.goto("https://the-internet.herokuapp.com/frames")
    page.wait_for_load_state("domcontentloaded")

    nested_link = page.locator("a[href='/nested_frames']")
    iframe_link = page.locator("a[href='/iframe']")

    expect(nested_link).to_be_visible(timeout=10000)
    expect(iframe_link).to_be_visible(timeout=10000)
