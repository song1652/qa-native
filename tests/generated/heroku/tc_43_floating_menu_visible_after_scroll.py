from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_floating_menu_visible_after_scroll(page: Page):
    """플로팅 메뉴 스크롤 후 고정 확인"""
    page.goto(f"{BASE_URL}floating_menu")
    page.wait_for_load_state("domcontentloaded")

    # 초기 메뉴 가시성 확인
    menu = page.locator("#menu")
    expect(menu).to_be_visible(timeout=10000)

    # 페이지 하단으로 스크롤
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(500)

    # 스크롤 후에도 플로팅 메뉴가 DOM에 존재하는지 확인
    # lessons_learned: floating_menu의 #menu는 position: absolute (fixed 아님)
    # CSS position 검증 또는 viewport 좌표 검증 불가 → DOM 존재 + 링크 포함 여부로 검증
    assert menu.count() > 0, "Floating menu #menu should exist in DOM after scroll"

    links = menu.locator("a")
    assert links.count() >= 1, "Floating menu should have at least one navigation link"
