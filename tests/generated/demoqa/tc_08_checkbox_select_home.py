"""Playwright 테스트 — test_checkbox_select_home (tc_08)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_checkbox_select_home(page):
    """Select Home checkbox to select all children"""
    page.goto(BASE_URL + "/checkbox")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(1000)

    # Click Home checkbox
    page.locator(".rc-tree-checkbox[aria-label='Select Home']").click()
    page.wait_for_timeout(500)

    # Check that Home is checked
    home_cb = page.locator(".rc-tree-checkbox[aria-label='Select Home']")
    expect(home_cb).to_have_attribute("aria-checked", "true", timeout=5000)
