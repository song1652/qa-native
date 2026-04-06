"""Playwright 테스트 — test_form_modal_close (tc_39)"""
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


def test_form_modal_close(page):
    """Submit form and close the result modal"""
    page.goto(BASE_URL + "/automation-practice-form")
    page.wait_for_load_state("domcontentloaded")
    _remove_form_overlays(page)

    page.locator("#firstName").fill("John")
    page.locator("#lastName").fill("Doe")
    page.locator("label[for='gender-radio-1']").click()
    page.locator("#userNumber").fill("1234567890")

    page.locator("#submit").scroll_into_view_if_needed()
    page.wait_for_timeout(300)
    page.evaluate("document.querySelector('#submit').click()")

    expect(page.locator(".modal-title")).to_be_visible(timeout=10000)
    expect(page.locator(".modal-title")).to_contain_text("Thanks for submitting the form")

    # Close modal by clicking the backdrop (outside modal content)
    # The #closeLargeModal button doesn't trigger React handler in headless
    page.wait_for_timeout(500)
    page.mouse.click(10, 10)
    page.wait_for_timeout(1000)

    # Verify modal is gone
    expect(page.locator(".modal-dialog")).not_to_be_visible(timeout=15000)
