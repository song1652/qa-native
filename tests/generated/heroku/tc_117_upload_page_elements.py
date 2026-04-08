"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_117_upload_page_elements (tc_117)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_117_upload_page_elements(page):
    """업로드 페이지에서 #file-upload, #file-submit, #drag-drop-upload 요소 존재 확인"""
    page.goto(BASE_URL + "upload")
    page.wait_for_load_state("domcontentloaded")
    expect(page.locator("#file-upload")).to_be_visible(timeout=5000)
    expect(page.locator("#file-submit")).to_be_visible(timeout=5000)
    expect(page.locator("#drag-drop-upload")).to_be_visible(timeout=5000)
