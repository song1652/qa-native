"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_73_status_code_301 (tc_73)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_73_status_code_301(page):
    """상태 코드 301 페이지 확인"""
    page.goto(BASE_URL + "status_codes")

    page.locator("a", has_text="301").click()
    page.wait_for_load_state("domcontentloaded")

    # 301 redirects automatically — verify we landed somewhere and body is visible
    expect(page.locator("body")).to_be_visible(timeout=10000)

    # The page after redirect should reference 301
    body_text = page.locator("body").inner_text()
    assert "301" in body_text, f"Expected '301' in page body, got: {body_text[:200]}"
