"""Playwright 테스트 — test_new_tab (tc_41)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_new_tab(page):
    """New tab opens with sample page text"""
    page.goto(BASE_URL + "/browser-windows")
    page.wait_for_load_state("domcontentloaded")

    with page.context.expect_page() as new_page_info:
        page.locator("#tabButton").click()
    new_page = new_page_info.value
    new_page.wait_for_load_state("domcontentloaded")

    expect(new_page.locator("#sampleHeading")).to_have_text(
        "This is a sample page", timeout=10000
    )
    new_page.close()
