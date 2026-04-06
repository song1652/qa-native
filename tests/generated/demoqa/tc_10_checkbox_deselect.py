"""Playwright 테스트 — test_checkbox_deselect (tc_10)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_checkbox_deselect(page):
    """Deselect Home checkbox after selecting"""
    page.goto(BASE_URL + "/checkbox")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(1000)

    home_cb = page.locator(".rc-tree-checkbox[aria-label='Select Home']")
    home_cb.click()
    page.wait_for_timeout(300)
    expect(home_cb).to_have_attribute("aria-checked", "true", timeout=5000)

    home_cb.click()
    page.wait_for_timeout(300)
    expect(home_cb).to_have_attribute("aria-checked", "false", timeout=5000)
