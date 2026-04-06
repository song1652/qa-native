"""Playwright 테스트 — test_new_window_message (tc_43)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_new_window_message(page):
    """New window message shows text"""
    page.goto(BASE_URL + "/browser-windows")
    page.wait_for_load_state("domcontentloaded")

    with page.context.expect_page() as new_page_info:
        page.locator("#messageWindowButton").click()
    new_page = new_page_info.value
    new_page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(1000)

    content = new_page.content()
    assert len(content) > 50, "New window should have content"
    new_page.close()
