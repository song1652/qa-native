"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_40_file_download_links (tc_40)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_tc_40_file_download_links(page):
    """다운로드 페이지에서 파일 링크 최소 1개 존재 및 href 확인"""
    page.goto("https://the-internet.herokuapp.com/download")
    links = page.locator("#content a")
    expect(links.first).to_be_visible(timeout=10000)
    link_count = links.count()
    assert link_count >= 1, f"Expected at least 1 download link, got {link_count}"
    # Verify all links contain 'download' in href (relative path pattern)
    for i in range(link_count):
        href = links.nth(i).get_attribute("href")
        assert href is not None and "download" in href, (
            f"Link {i} href does not contain 'download': {href}"
        )
