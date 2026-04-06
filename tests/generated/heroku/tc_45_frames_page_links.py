"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_45_frames_page_links (tc_45)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_frames_page_links(page):
    """Frames 페이지 링크 목록 확인"""
    page.goto(BASE_URL + "frames")
    page.wait_for_load_state("networkidle")

    # "Nested Frames" 링크 존재 확인
    nested_frames_link = page.locator("a[href='/nested_frames']")
    expect(nested_frames_link).to_be_visible(timeout=10000)

    # "iFrame" 링크 존재 확인
    iframe_link = page.locator("a[href='/iframe']")
    expect(iframe_link).to_be_visible(timeout=10000)
