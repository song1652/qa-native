from playwright.sync_api import expect
from pathlib import Path

BASE_URL = "https://demoqa.com"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"
_RM_ADS_FOOTER = (
    "document.querySelectorAll("
    "'ins.adsbygoogle,iframe[src*=google],iframe[src*=doubleclick],"
    "#adplus-anchor,.ad-container,#fixedban,footer'"
    ").forEach(e=>e.remove())"
)


def test_form_required_only(page):
    page.goto(f"{BASE_URL}/automation-practice-form", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)
    page.evaluate(_RM_ADS_FOOTER)

    # First Name (required)
    page.locator("#firstName").fill("Jane")

    # Last Name (required)
    page.locator("#lastName").fill("Smith")

    # Gender: Female (required) — JS click on label to avoid overlay
    page.evaluate("document.querySelector('label[for=gender-radio-2]').click()")

    # Mobile (required)
    page.locator("#userNumber").fill("9876543210")

    # Submit
    page.locator("#submit").click()

    # Verify modal appears with submitted values
    modal = page.locator(".modal-content")
    expect(modal).to_be_visible(timeout=10000)
    expect(modal).to_contain_text("Thanks for submitting the form")
    expect(modal).to_contain_text("Jane Smith")
    expect(modal).to_contain_text("Female")
    expect(modal).to_contain_text("9876543210")
