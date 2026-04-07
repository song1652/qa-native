"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_21_ab_test_page_load (tc_21)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_tc_21_ab_test_page_load(page):
    """A/B 테스트 페이지 로드 시 제목과 본문 텍스트 존재 확인"""
    page.goto("https://the-internet.herokuapp.com/abtest")
    heading = page.locator("div.example h3")
    expect(heading).to_be_visible(timeout=10000)
    heading_text = heading.inner_text()
    assert "A/B Test" in heading_text
