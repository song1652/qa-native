"""Playwright 테스트 — test_form_state_dependent_city (tc_116)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"

def _remove_form_overlays(page):
    """Remove footer/ads that intercept form clicks."""
    page.evaluate(
        "document.querySelector('footer')?.remove();"
        "document.querySelector('#fixedban')?.remove();"
        "document.querySelectorAll('iframe:not([id=frame1]):not([id=frame2]),"
        " ins.adsbygoogle, #adplus-anchor, .ad').forEach(e => e.remove())"
    )


def test_form_state_dependent_city(page):
    """Form state dependent city options"""
    page.goto(BASE_URL + "/automation-practice-form")
    page.wait_for_load_state("domcontentloaded")
    _remove_form_overlays(page)

    page.locator("#state").scroll_into_view_if_needed()
    page.locator("#state").click()
    page.locator("#react-select-3-input").fill("Uttar Pradesh")
    page.locator("#react-select-3-input").press("Enter")
    page.wait_for_timeout(300)

    page.locator("#city").click()
    page.wait_for_timeout(500)

    expect(page.locator(".css-26l3qy-menu, [class*='menu']").last).to_contain_text("Agra", timeout=5000)
