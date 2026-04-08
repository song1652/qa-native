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
    """리다이렉트 후 최종 URL이 /status_codes이고 Status Codes 제목 표시 확인"""
    page.goto("https://the-internet.herokuapp.com/redirector")
    page.wait_for_load_state("domcontentloaded")

    page.locator("#redirect").click()
    page.wait_for_load_state("domcontentloaded")

    expect(page).to_have_url("https://the-internet.herokuapp.com/status_codes", timeout=10000)
    expect(page.locator("h3")).to_contain_text("Status Codes", timeout=5000)
