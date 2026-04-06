"""Playwright 테스트 — test_menu_main_items (tc_69)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_menu_main_items(page):
    """Menu main items display"""
    page.goto(BASE_URL + "/menu")
    page.wait_for_load_state("domcontentloaded")

    expect(page.locator("a:has-text('Main Item 1')")).to_be_visible(timeout=5000)
    expect(page.locator("a:has-text('Main Item 2')")).to_be_visible(timeout=5000)
    expect(page.locator("a:has-text('Main Item 3')")).to_be_visible(timeout=5000)
