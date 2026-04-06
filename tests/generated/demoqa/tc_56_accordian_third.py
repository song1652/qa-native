"""Playwright 테스트 — test_accordian_third (tc_56)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_accordian_third(page):
    """Accordion third section opens on click"""
    page.goto(BASE_URL + "/accordian")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(1000)

    third_btn = page.locator(".accordion-button").nth(2)
    third_btn.click()
    page.wait_for_timeout(1000)

    expect(third_btn).to_have_attribute("aria-expanded", "true", timeout=5000)
