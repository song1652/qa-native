"""Playwright 테스트 — test_homepage_widgets_card (tc_94)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_homepage_widgets_card(page):
    """Homepage widgets card"""
    page.goto(BASE_URL)
    page.wait_for_load_state("domcontentloaded")

    page.locator("h5:has-text('Widgets')").click()
    page.wait_for_load_state("domcontentloaded")

    assert "/widgets" in page.url
