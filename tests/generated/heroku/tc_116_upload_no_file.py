from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_upload_no_file(page: Page):
    """TC-116: 파일 선택 없이 업로드 시도 - 오류 또는 서버 에러 표시"""
    page.goto("https://the-internet.herokuapp.com/upload")
    page.wait_for_load_state("domcontentloaded")

    page.locator("#file-submit").click()

    # 파일 미선택 업로드 시 Internal Server Error 또는 에러 응답 확인
    # 응답이 올 때까지 대기
    page.wait_for_load_state("domcontentloaded", timeout=10000)

    body_text = page.locator("body").inner_text()
    assert (
        "Internal Server Error" in body_text
        or "error" in body_text.lower()
        or page.url != "https://the-internet.herokuapp.com/upload"
    ), f"Expected error indication after upload with no file, got body: {body_text[:200]}"
