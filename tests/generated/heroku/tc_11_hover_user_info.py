"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: test_hover_user_info (tc_11)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_hover_user_info(page):
    """호버 시 사용자 정보 표시 — 첫 번째 이미지 호버 후 name:user1, View profile 확인"""
    page.goto(BASE_URL + "hovers")

    # lessons_learned: .figcaption CSS 클래스 사용 (not <figcaption> tag)
    figure = page.locator(".figure").nth(0)
    figure.hover()

    caption = figure.locator(".figcaption")
    expect(caption).to_be_visible(timeout=5000)
    expect(caption.locator("h5")).to_contain_text("name: user1", timeout=5000)
    expect(caption.locator("a")).to_contain_text("View profile", timeout=5000)
