"""Playwright 테스트 — test_dynamic_visible_after_5s (tc_24)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_dynamic_visible_after_5s(page):
    """Button becomes visible after 5 seconds"""
    page.goto(BASE_URL + "/dynamic-properties")
    page.wait_for_load_state("domcontentloaded")

    btn = page.locator("#visibleAfter")
    expect(btn).to_be_visible(timeout=10000)
