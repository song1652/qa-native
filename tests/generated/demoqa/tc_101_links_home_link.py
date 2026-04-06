"""Playwright 테스트 — test_links_home_link (tc_101)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_links_home_link(page):
    """Links home link opens new tab"""
    page.goto(BASE_URL + "/links")
    page.wait_for_load_state("domcontentloaded")

    with page.context.expect_page() as new_page_info:
        page.locator("#simpleLink").click()
    new_page = new_page_info.value
    new_page.wait_for_load_state("domcontentloaded")

    assert "demoqa.com" in new_page.url
    new_page.close()
