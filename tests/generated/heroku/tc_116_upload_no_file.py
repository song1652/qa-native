"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_116_upload_no_file (tc_116)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_116_upload_no_file(page):
    """파일 미선택 상태에서 Upload 클릭 시 에러 발생 확인"""
    page.goto(BASE_URL + "upload")
    page.wait_for_load_state("domcontentloaded")
    page.locator("#file-submit").click()
    # Server returns Internal Server Error when no file is selected
    expect(page.locator("body")).to_be_visible(timeout=10000)
    body_text = page.locator("body").inner_text()
    assert "Internal Server Error" in body_text or "error" in body_text.lower()
