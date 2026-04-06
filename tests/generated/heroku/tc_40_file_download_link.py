"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_40_file_download_link (tc_40)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
BASE_URL = "https://the-internet.herokuapp.com/"


def test_file_download_link(page):
    """파일 다운로드 링크 확인"""
    page.goto(BASE_URL + "download")
    page.wait_for_load_state("networkidle")

    # #content 내 모든 링크 확인
    links = page.locator("#content a")
    count = links.count()
    assert count >= 1, f"Expected at least 1 download link, got {count}"

    # 각 링크의 href 속성 확인
    for i in range(count):
        href = links.nth(i).get_attribute("href")
        assert href is not None and len(href) > 0, f"Link {i} has no href"
        assert "download" in href, (
            f"Link {i} href does not contain 'download': {href}"
        )
