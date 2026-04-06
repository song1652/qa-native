"""Playwright 테스트 — test_menu_submenu_hover (tc_70)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_menu_submenu_hover(page):
    """Menu submenu hover"""
    page.goto(BASE_URL + "/menu")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(1000)

    # Hover Main Item 2
    main2 = page.locator("#nav > li:nth-child(2) > a")
    main2.hover()
    page.wait_for_timeout(1000)

    # Submenu should be visible
    sub = page.locator("#nav > li:nth-child(2) > ul > li > a")
    expect(sub.first).to_be_visible(timeout=5000)
