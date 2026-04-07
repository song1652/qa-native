"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_42_floating_menu_display (tc_42)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_42_floating_menu_display(page):
    """플로팅 메뉴 DOM 존재 및 Home/News/Contact/About 항목 확인"""
    page.goto("https://the-internet.herokuapp.com/floating_menu")
    page.wait_for_load_state("domcontentloaded")

    menu = page.locator("#menu")
    expect(menu).to_be_visible(timeout=10000)

    for label in ["Home", "News", "Contact", "About"]:
        link = menu.locator("a", has_text=label)
        expect(link).to_be_visible(timeout=5000)
