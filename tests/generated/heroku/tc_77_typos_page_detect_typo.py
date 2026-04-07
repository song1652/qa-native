"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_77_typos_page_detect_typo (tc_77)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_77_typos_page_detect_typo(page):
    """Typos 페이지 두 번째 단락 읽기 및 페이지 정상 로드 확인"""
    page.goto("https://the-internet.herokuapp.com/typos")
    page.wait_for_load_state("domcontentloaded")

    second_paragraph = page.locator("#content p").nth(1)
    expect(second_paragraph).to_be_visible(timeout=5000)

    text = second_paragraph.inner_text()
    assert len(text.strip()) > 0
