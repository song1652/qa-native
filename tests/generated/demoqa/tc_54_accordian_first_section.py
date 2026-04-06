"""Playwright 테스트 — test_accordian_first_section (tc_54)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_accordian_first_section(page):
    """Verify first accordion section is open by default"""
    page.goto(BASE_URL + "/accordian")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(1000)

    # First accordion item button should have aria-expanded=true
    first_btn = page.locator(".accordion-button").first
    expect(first_btn).to_have_attribute("aria-expanded", "true", timeout=5000)

    # First content should be visible (has .show class)
    first_body = page.locator(".accordion-collapse.show .accordion-body")
    expect(first_body).to_be_visible(timeout=5000)

    # Other sections should be collapsed
    buttons = page.locator(".accordion-button")
    for i in range(1, buttons.count()):
        expect(buttons.nth(i)).to_have_attribute("aria-expanded", "false", timeout=3000)
