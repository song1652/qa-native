"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_22_ab_test_content_variation (tc_22)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_tc_22_ab_test_content_variation(page):
    """A/B 테스트 페이지 새로고침 후 제목 변형 확인"""
    page.goto("https://the-internet.herokuapp.com/abtest")
    heading = page.locator("div.example h3")
    expect(heading).to_be_visible(timeout=10000)
    heading_text = heading.inner_text()
    assert "A/B Test" in heading_text
    # Reload and check structure is maintained (Control or Variation 1)
    page.reload()
    heading2 = page.locator("div.example h3")
    expect(heading2).to_be_visible(timeout=10000)
    heading_text2 = heading2.inner_text()
    assert "A/B Test" in heading_text2
