"""Playwright 테스트 — test_checkbox_collapse_all (tc_07)"""
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


def test_checkbox_collapse_all(page):
    """Collapse all checkbox tree after expanding"""
    page.goto(BASE_URL + "/checkbox")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(1000)

    _expand_all(page)
    expect(page.locator(".rc-tree-title:has-text('Notes')")).to_be_visible(timeout=5000)

    # Collapse all by clicking open switchers (bottom-up works, but collapsing root is easier)
    # Click the Home switcher to collapse everything
    home_switcher = page.locator(".rc-tree-switcher_open").first
    home_switcher.click()
    page.wait_for_timeout(500)

    expect(page.locator(".rc-tree-title:has-text('Notes')")).not_to_be_visible(timeout=5000)
    expect(page.locator(".rc-tree-title:has-text('Home')")).to_be_visible(timeout=5000)
