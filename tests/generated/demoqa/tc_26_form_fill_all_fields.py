"""Playwright 테스트 — test_form_fill_all_fields (tc_26)"""
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


def test_form_fill_all_fields(page):
    """Form fill all fields and submit"""
    page.goto(BASE_URL + "/automation-practice-form")
    page.wait_for_load_state("domcontentloaded")
    _remove_form_overlays(page)

    page.locator("#firstName").fill("John")
    page.locator("#lastName").fill("Doe")
    page.locator("#userEmail").fill("john@test.com")
    page.locator("label[for='gender-radio-1']").click()
    page.locator("#userNumber").fill("1234567890")

    # Subject
    page.locator("#subjectsInput").fill("Ma")
    page.locator(".subjects-auto-complete__option:has-text('Maths')").click()

    # Hobby
    page.locator("label[for='hobbies-checkbox-1']").click()

    # Current Address
    page.locator("#currentAddress").fill("123 Test Street")

    # State and City
    page.locator("#state").scroll_into_view_if_needed()
    _remove_form_overlays(page)
    page.locator("#state").click()
    page.locator("#react-select-3-input").fill("NCR")
    page.locator("#react-select-3-input").press("Enter")
    page.wait_for_timeout(300)
    page.locator("#city").click()
    page.locator("#react-select-4-input").fill("Delhi")
    page.locator("#react-select-4-input").press("Enter")

    # Submit
    page.locator("#submit").scroll_into_view_if_needed()
    page.evaluate("document.querySelector('#submit').click()")

    expect(page.locator(".modal-title")).to_be_visible(timeout=10000)
    expect(page.locator(".modal-title")).to_contain_text("Thanks for submitting the form")
