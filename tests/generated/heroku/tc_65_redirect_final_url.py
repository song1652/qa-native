"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_65_redirect_final_url (tc_65)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_65_redirect_final_url(page):
    """리다이렉트 최종 URL 확인"""
    page.goto(BASE_URL + "redirector")

    page.locator("a", has_text="here").click()
    page.wait_for_load_state("domcontentloaded")

    expect(page).to_have_url(BASE_URL + "status_codes", timeout=10000)

    heading = page.locator("h3")
    expect(heading).to_contain_text("Status Codes", timeout=10000)
