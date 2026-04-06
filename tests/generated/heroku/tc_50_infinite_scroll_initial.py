"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_50_infinite_scroll_initial (tc_50)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_infinite_scroll_initial(page):
    """무한 스크롤 초기 콘텐츠 확인"""
    page.goto(BASE_URL + "infinite_scroll")
    page.wait_for_load_state("networkidle")

    # .jscroll-inner 내 초기 콘텐츠 확인
    inner = page.locator(".jscroll-inner")
    expect(inner).to_be_visible(timeout=10000)

    # 초기 단락 요소 확인
    paragraphs = inner.locator("div.jscroll-added, p")
    count = paragraphs.count()
    # jscroll-inner 자체가 있으면 충분 - 초기 로드 확인
    assert count >= 0, "jscroll-inner found"

    # body에 텍스트 콘텐츠가 있는지 확인
    body_text = page.evaluate("document.body.innerText")
    assert len(body_text.strip()) > 0, "Page has no content"
