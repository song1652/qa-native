"""Playwright 테스트 — test_autocomplete_multi (tc_57)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_autocomplete_multi(page):
    """Auto complete multi color selection"""
    page.goto(BASE_URL + "/auto-complete")
    page.wait_for_load_state("domcontentloaded")

    multi_input = page.locator("#autoCompleteMultipleInput")
    multi_input.fill("Re")
    page.wait_for_timeout(500)
    page.locator(".auto-complete__option:has-text('Red')").click()
    page.wait_for_timeout(300)

    multi_input.fill("Bl")
    page.wait_for_timeout(500)
    page.locator(".auto-complete__option:has-text('Blue')").click()

    tags = page.locator(".auto-complete__multi-value__label")
    expect(tags).to_have_count(2, timeout=5000)
