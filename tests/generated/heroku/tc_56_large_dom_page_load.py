"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_56_large_dom_page_load (tc_56)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_56_large_dom_page_load(page):
    """대규모 DOM 페이지 로드 및 Large & Deep DOM 제목 확인"""
    page.goto("https://the-internet.herokuapp.com/large")
    page.wait_for_load_state("domcontentloaded")

    heading = page.locator("#content h3")
    expect(heading).to_be_visible(timeout=15000)
    expect(heading).to_contain_text("Large & Deep DOM", timeout=5000)
