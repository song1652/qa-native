"""Playwright 테스트 — test_homepage_elements_card (tc_92)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_homepage_elements_card(page):
    """Homepage elements card"""
    page.goto(BASE_URL)
    page.wait_for_load_state("domcontentloaded")

    page.locator("h5:has-text('Elements')").click()
    page.wait_for_load_state("domcontentloaded")

    assert "/elements" in page.url
