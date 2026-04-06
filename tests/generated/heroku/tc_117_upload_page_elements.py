from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_upload_page_elements(page: Page):
    """TC-117: 업로드 페이지 요소 확인 - file input, upload 버튼, drag & drop 영역"""
    page.goto("https://the-internet.herokuapp.com/upload")
    page.wait_for_load_state("domcontentloaded")

    # 파일 선택 input 확인
    file_input = page.locator("#file-upload")
    expect(file_input).to_be_attached(timeout=10000)

    # Upload 버튼 확인
    upload_btn = page.locator("#file-submit")
    expect(upload_btn).to_be_visible(timeout=10000)

    # 드래그 앤 드롭 영역 확인
    drag_drop = page.locator("#drag-drop-upload")
    expect(drag_drop).to_be_visible(timeout=10000)
