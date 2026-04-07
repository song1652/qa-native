"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_41_file_download_execute (tc_41)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_41_file_download_execute(page):
    """첫 번째 다운로드 링크 클릭 시 파일 다운로드 이벤트 발생 확인"""
    page.goto("https://the-internet.herokuapp.com/download")
    page.wait_for_load_state("domcontentloaded")

    first_link = page.locator("#content a").first
    link_text = first_link.inner_text()

    with page.expect_download() as download_info:
        first_link.click()

    download = download_info.value
    assert download.suggested_filename != ""
    assert link_text in download.suggested_filename
