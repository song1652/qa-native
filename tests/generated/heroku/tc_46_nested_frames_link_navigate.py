"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_46_nested_frames_link_navigate (tc_46)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_nested_frames_link_navigate(page):
    """Nested Frames 링크 이동 확인"""
    page.goto(BASE_URL + "frames")
    page.wait_for_load_state("networkidle")

    # "Nested Frames" 링크 클릭
    nested_link = page.locator("a[href='/nested_frames']")
    nested_link.click()
    page.wait_for_load_state("load")

    # /nested_frames 페이지로 이동했는지 확인
    expect(page).to_have_url(BASE_URL + "nested_frames", timeout=10000)
