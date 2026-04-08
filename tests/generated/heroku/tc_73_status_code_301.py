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
    """301 링크 클릭 후 상태 코드 설명 페이지 확인"""
    page.goto("https://the-internet.herokuapp.com/status_codes")
    page.wait_for_load_state("domcontentloaded")

    page.get_by_role("link", name="301").click()
    page.wait_for_load_state("domcontentloaded")

    expect(page.locator("#content")).to_contain_text(
        "This page returned a 301 status code", timeout=5000
    )
