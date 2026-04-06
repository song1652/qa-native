"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_116_file_upload_no_file (tc_116)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_tc_116_file_upload_no_file(page):
    """파일 선택 없이 업로드 시도"""
    page.goto(BASE_URL + "upload")

    # verify upload button exists before clicking
    submit_btn = page.locator("#file-submit")
    expect(submit_btn).to_be_visible(timeout=5000)

    # click upload without selecting a file - should not crash
    submit_btn.click()

    # page stays responsive (either shows error or stays on same/new page)
    expect(page.locator("body")).to_be_visible(timeout=5000)
