"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_41_file_download_execute (tc_41)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
BASE_URL = "https://the-internet.herokuapp.com/"


def test_file_download_execute(page):
    """파일 다운로드 실행"""
    page.goto(BASE_URL + "download")
    page.wait_for_load_state("networkidle")

    # 첫 번째 다운로드 링크 텍스트 저장
    first_link = page.locator("#content a").first
    link_text = first_link.inner_text().strip()

    # 다운로드 이벤트 대기하며 첫 번째 링크 클릭
    with page.expect_download(timeout=15000) as download_info:
        first_link.click()

    download = download_info.value
    # 다운로드된 파일명이 링크 텍스트와 일치
    assert download.suggested_filename == link_text, (
        f"Expected filename '{link_text}', got '{download.suggested_filename}'"
    )
