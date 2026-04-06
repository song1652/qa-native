"""Playwright 테스트 — test_links_not_found_api (tc_104)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_links_not_found_api(page):
    """Links not found API call"""
    page.goto(BASE_URL + "/links")
    page.wait_for_load_state("domcontentloaded")

    page.locator("#invalid-url").click()
    expect(page.locator("#linkResponse")).to_contain_text("404", timeout=10000)
