from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_file_download_links_exist(page: Page):
    """파일 다운로드 링크 확인"""
    page.goto(f"{BASE_URL}download")
    page.wait_for_load_state("domcontentloaded")

    # 다운로드 가능한 파일 링크 목록 확인
    # lessons_learned: href는 "download/filename" 상대 경로
    download_links = page.locator(".example a")
    expect(download_links.first).to_be_visible(timeout=10000)

    count = download_links.count()
    assert count >= 1, f"Expected at least 1 download link, got {count}"

    # 각 링크에 유효한 href가 설정되어 있는지 확인
    for i in range(count):
        link = download_links.nth(i)
        href = link.get_attribute("href")
        assert href is not None and "download" in href, (
            f"Link {i} has invalid href: {href}"
        )
