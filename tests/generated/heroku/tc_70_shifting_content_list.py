"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_70_shifting_content_list (tc_70)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_70_shifting_content_list(page):
    """Shifting Content 리스트 페이지에서 텍스트 콘텐츠 존재 확인 (li 없음, br 구분)"""
    page.goto("https://the-internet.herokuapp.com/shifting_content/list")
    page.wait_for_load_state("domcontentloaded")

    # No <li> elements — content is <br><br> separated text inside .large-6
    content = page.locator(".large-6")
    expect(content).to_be_visible(timeout=10000)

    # Verify the text content is present and non-empty
    text = content.inner_text()
    assert len(text.strip()) > 0
