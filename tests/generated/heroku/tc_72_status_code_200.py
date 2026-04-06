"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_72_status_code_200 (tc_72)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_72_status_code_200(page):
    """상태 코드 200 페이지 확인"""
    page.goto(BASE_URL + "status_codes")

    page.locator("a", has_text="200").click()
    page.wait_for_load_state("domcontentloaded")

    body = page.locator("body")
    expect(body).to_contain_text("200", timeout=10000)
    expect(body).to_contain_text("status code", ignore_case=True, timeout=10000)
