"""Playwright 테스트 — test_checkbox_expand_single_node (tc_118)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_checkbox_expand_single_node(page):
    """Checkbox expand single node"""
    page.goto(BASE_URL + "/checkbox")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(1000)

    # Click Home switcher to expand one level
    page.locator(".rc-tree-switcher_close").first.click()
    page.wait_for_timeout(500)

    expect(page.locator(".rc-tree-title:has-text('Desktop')")).to_be_visible(timeout=5000)
    expect(page.locator(".rc-tree-title:has-text('Documents')")).to_be_visible(timeout=5000)
    expect(page.locator(".rc-tree-title:has-text('Downloads')")).to_be_visible(timeout=5000)
