"""Playwright 테스트 — test_dynamic_button_enabled_after_5s (tc_22)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_dynamic_button_enabled_after_5s(page):
    """Button becomes enabled after 5 seconds"""
    page.goto(BASE_URL + "/dynamic-properties")
    page.wait_for_load_state("domcontentloaded")

    btn = page.locator("#enableAfter")
    expect(btn).to_be_disabled(timeout=3000)
    expect(btn).to_be_enabled(timeout=10000)
