"""Playwright 테스트 — test_tooltip_link (tc_68)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tooltip_link(page):
    """Tooltip contrary link hover"""
    page.goto(BASE_URL + "/tool-tips")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(1000)

    contrary = page.locator("#texToolTopContainer a").first
    contrary.scroll_into_view_if_needed()
    contrary.hover()
    page.wait_for_timeout(1500)

    tooltip = page.locator(".tooltip-inner, [role='tooltip']")
    expect(tooltip.first).to_be_visible(timeout=5000)
