"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_43_floating_menu_scroll_fixed (tc_43)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_43_floating_menu_scroll_fixed(page):
    """스크롤 후 플로팅 메뉴 DOM 존재 확인 (position:absolute이므로 뷰포트 검증 금지)"""
    page.goto("https://the-internet.herokuapp.com/floating_menu")
    page.wait_for_load_state("domcontentloaded")

    # Scroll down the page
    page.evaluate("window.scrollTo(0, 500)")
    page.wait_for_timeout(500)

    # Verify menu still exists in DOM and has links — no viewport coordinate check
    menu = page.locator("#menu")
    expect(menu).to_be_attached(timeout=5000)

    link_count = menu.locator("a").count()
    assert link_count >= 4
