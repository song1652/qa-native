"""Playwright 테스트 — test_accordian_toggle (tc_55)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_accordian_toggle(page):
    """Click second section and verify first closes"""
    page.goto(BASE_URL + "/accordian")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(1000)

    # First section should be open
    first_btn = page.locator(".accordion-button").nth(0)
    expect(first_btn).to_have_attribute("aria-expanded", "true", timeout=5000)

    # Click second section
    second_btn = page.locator(".accordion-button").nth(1)
    second_btn.click()
    page.wait_for_timeout(1000)

    # Second should be open, first should be closed
    expect(second_btn).to_have_attribute("aria-expanded", "true", timeout=5000)
    expect(first_btn).to_have_attribute("aria-expanded", "false", timeout=5000)
