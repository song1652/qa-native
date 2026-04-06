"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_75_status_code_500 (tc_75)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_75_status_code_500(page):
    """상태 코드 500 페이지 확인"""
    page.goto(BASE_URL + "status_codes")

    page.locator("a", has_text="500").click()
    page.wait_for_load_state("domcontentloaded")

    body = page.locator("body")
    expect(body).to_contain_text("500", timeout=10000)
    expect(body).to_contain_text("status code", ignore_case=True, timeout=10000)
