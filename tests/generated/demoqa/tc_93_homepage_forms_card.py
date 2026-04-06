"""Playwright 테스트 — test_homepage_forms_card (tc_93)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_homepage_forms_card(page):
    """Homepage forms card"""
    page.goto(BASE_URL)
    page.wait_for_load_state("domcontentloaded")

    page.locator("h5:has-text('Forms')").click()
    page.wait_for_load_state("domcontentloaded")

    assert "/forms" in page.url
