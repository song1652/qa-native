"""Playwright 테스트 — test_sidebar_navigation (tc_95)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_sidebar_navigation(page):
    """Sidebar navigation"""
    page.goto(BASE_URL + "/elements")
    page.wait_for_load_state("domcontentloaded")

    page.locator("li:has-text('Check Box') >> span.text").click()
    assert "/checkbox" in page.url

    page.locator("li:has-text('Radio Button') >> span.text").click()
    assert "/radio-button" in page.url

    page.locator("li:has-text('Web Tables') >> span.text").click()
    assert "/webtables" in page.url
