"""Playwright 테스트 — test_form_state_city_select (tc_36)"""
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


def test_form_state_city_select(page):
    """Select state and city dropdowns"""
    page.goto(BASE_URL + "/automation-practice-form")
    page.wait_for_load_state("domcontentloaded")
    _remove_form_overlays(page)

    page.locator("#state").scroll_into_view_if_needed()
    page.wait_for_timeout(300)
    page.locator("#state").click()
    page.locator("#react-select-3-input").fill("NCR")
    page.locator("#react-select-3-input").press("Enter")
    page.wait_for_timeout(300)

    page.locator("#city").click()
    page.locator("#react-select-4-input").fill("Delhi")
    page.locator("#react-select-4-input").press("Enter")

    expect(page.locator("#state")).to_contain_text("NCR", timeout=5000)
    expect(page.locator("#city")).to_contain_text("Delhi", timeout=5000)
