"""Playwright 테스트 — test_form_required_only (tc_27)"""
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


def test_form_required_only(page):
    """Form required fields only"""
    page.goto(BASE_URL + "/automation-practice-form")
    page.wait_for_load_state("domcontentloaded")
    _remove_form_overlays(page)

    page.locator("#firstName").fill("Jane")
    page.locator("#lastName").fill("Smith")
    page.locator("label[for='gender-radio-2']").click()
    page.locator("#userNumber").fill("9876543210")

    page.locator("#submit").scroll_into_view_if_needed()
    page.evaluate("document.querySelector('#submit').click()")

    expect(page.locator(".modal-title")).to_be_visible(timeout=10000)
    expect(page.locator(".modal-title")).to_contain_text("Thanks for submitting the form")
