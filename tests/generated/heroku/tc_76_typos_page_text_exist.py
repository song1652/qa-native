"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_76_typos_page_text_exist (tc_76)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_76_typos_page_text_exist(page):
    """Typos 페이지 텍스트 존재 확인"""
    page.goto(BASE_URL + "typos")

    # Verify page title heading
    expect(page.locator("h3")).to_contain_text("Typos", timeout=10000)

    # Verify body text paragraphs exist in #content
    paragraphs = page.locator("#content p")
    expect(paragraphs).to_have_count(2, timeout=10000)
    expect(paragraphs.first).to_be_visible()
    expect(paragraphs.nth(1)).to_be_visible()
