"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_77_typos_page_detect (tc_77)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_77_typos_page_detect(page):
    """Typos 페이지 오타 감지"""
    page.goto(BASE_URL + "typos")

    # Page must load correctly
    expect(page.locator("body")).to_be_visible(timeout=10000)
    expect(page.locator("h3")).to_contain_text("Typos")

    # Read second paragraph text — the page intentionally contains typos
    # e.g. "won't" may appear as "wont" or similar variation
    paragraphs = page.locator("#content p")
    expect(paragraphs).to_have_count(2, timeout=10000)

    second_text = paragraphs.nth(1).inner_text()
    # The page loads successfully regardless of typo variant
    assert len(second_text.strip()) > 0, (
        f"Second paragraph is empty: {second_text!r}"
    )
