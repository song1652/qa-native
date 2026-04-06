"""Playwright 테스트 — test_tooltip_textfield (tc_67)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tooltip_textfield(page):
    """Tooltip text field hover"""
    page.goto(BASE_URL + "/tool-tips")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(1000)

    page.locator("#toolTipTextField").hover()
    page.wait_for_timeout(1500)

    tooltip = page.locator(".tooltip-inner, [role='tooltip']")
    expect(tooltip.first).to_be_visible(timeout=5000)
