"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_57_large_dom_element_access (tc_57)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_57_large_dom_element_access(page):
    """대규모 DOM 특정 요소 접근"""
    page.goto(BASE_URL + "large", timeout=30000)

    # Access specific sibling element by ID: #sibling-1\.1
    sibling = page.locator("#sibling-1\\.1")
    expect(sibling).to_be_visible(timeout=15000)

    text = sibling.inner_text()
    assert "1.1" in text, f"Expected '1.1' in element text, got: {text}"
