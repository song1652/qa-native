"""Playwright 테스트 — test_checkbox_partial_select (tc_117)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def _expand_all(page):
    """Expand all tree nodes."""
    while True:
        closed = page.locator(".rc-tree-switcher_close")
        if closed.count() == 0:
            break
        closed.first.click()
        page.wait_for_timeout(300)


def test_checkbox_partial_select(page):
    """Checkbox partial select indeterminate state"""
    page.goto(BASE_URL + "/checkbox")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(1000)

    _expand_all(page)

    # Select Notes only
    page.locator(".rc-tree-checkbox[aria-label='Select Notes']").click()
    page.wait_for_timeout(300)

    # Desktop should be in half-checked/indeterminate state
    desktop_cb = page.locator(".rc-tree-checkbox[aria-label='Select Desktop']")
    aria = desktop_cb.get_attribute("aria-checked")
    assert aria == "mixed", f"Desktop should be indeterminate, got: {aria}"
