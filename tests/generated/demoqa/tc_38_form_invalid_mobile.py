"""Playwright 테스트 — test_form_invalid_mobile (tc_38)"""
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


def test_form_invalid_mobile(page):
    """Form invalid mobile validation"""
    page.goto(BASE_URL + "/automation-practice-form")
    page.wait_for_load_state("domcontentloaded")
    _remove_form_overlays(page)

    page.locator("#firstName").fill("John")
    page.locator("#lastName").fill("Doe")
    page.locator("label[for='gender-radio-1']").click()
    page.locator("#userNumber").fill("abc")

    page.locator("#submit").scroll_into_view_if_needed()
    page.evaluate("document.querySelector('#submit').click()")
    page.wait_for_timeout(500)

    expect(page.locator(".modal-title")).not_to_be_visible(timeout=3000)
