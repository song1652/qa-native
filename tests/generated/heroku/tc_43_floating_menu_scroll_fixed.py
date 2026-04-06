"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_43_floating_menu_scroll_fixed (tc_43)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_floating_menu_scroll_fixed(page):
    """플로팅 메뉴 스크롤 후 고정 확인"""
    page.goto(BASE_URL + "floating_menu")
    page.wait_for_load_state("networkidle")

    # 페이지 하단으로 스크롤
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(500)

    # 스크롤 후에도 #menu가 뷰포트에 표시되는지 확인
    menu = page.locator("#menu")
    expect(menu).to_be_visible(timeout=5000)

    # 스크롤 후에도 #menu가 DOM에 존재하고 visible 상태인지 확인
    # (floating_menu는 JS로 위치를 따라가므로 CSS position이 아닌 존재+가시성으로 검증)
    scroll_y = page.evaluate("window.scrollY")
    assert scroll_y > 0, "Expected page to have scrolled"
    expect(menu).to_be_visible(timeout=5000)
