from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_file_download_execute(page: Page):
    """파일 다운로드 실행"""
    page.goto(f"{BASE_URL}download")
    page.wait_for_load_state("domcontentloaded")

    # 첫 번째 다운로드 링크 텍스트 확인
    first_link = page.locator(".example a").first
    expect(first_link).to_be_visible(timeout=10000)
    link_text = first_link.inner_text().strip()

    # 다운로드 이벤트 대기하며 첫 번째 링크 클릭
    with page.expect_download(timeout=15000) as download_info:
        first_link.click()

    download = download_info.value
    # 다운로드된 파일명이 링크 텍스트와 일치하는지 확인
    assert download.suggested_filename == link_text, (
        f"Expected filename '{link_text}', got '{download.suggested_filename}'"
    )
