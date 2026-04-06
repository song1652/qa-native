from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_floating_menu_display(page: Page):
    """플로팅 메뉴 표시 확인"""
    page.goto(f"{BASE_URL}floating_menu")
    page.wait_for_load_state("domcontentloaded")

    # 플로팅 메뉴 요소 존재 확인
    menu = page.locator("#menu")
    expect(menu).to_be_visible(timeout=10000)

    # 메뉴 항목 텍스트 확인
    expect(menu).to_contain_text("Home", timeout=5000)
    expect(menu).to_contain_text("News", timeout=5000)
    expect(menu).to_contain_text("Contact", timeout=5000)
    expect(menu).to_contain_text("About", timeout=5000)
