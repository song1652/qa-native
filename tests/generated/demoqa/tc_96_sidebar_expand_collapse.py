"""Playwright 테스트 — test_sidebar_expand_collapse (tc_96)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_sidebar_expand_collapse(page):
    """Sidebar expand and collapse"""
    page.goto(BASE_URL + "/elements")
    page.wait_for_load_state("domcontentloaded")

    # Click Widgets group header
    widgets_header = page.locator(".element-group:has-text('Widgets') .header-wrapper")
    widgets_header.click()
    page.wait_for_timeout(500)

    expect(page.locator("li:has-text('Accordian')")).to_be_visible(timeout=5000)

    widgets_header.click()
    page.wait_for_timeout(500)

    expect(page.locator("li:has-text('Accordian')")).not_to_be_visible(timeout=5000)
