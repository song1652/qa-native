import os
import tempfile
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


def test_form_fill_all_fields(page):
    page.goto(f"{BASE_URL}/automation-practice-form", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)
    page.evaluate(_RM_ADS_FOOTER)

    # First Name
    page.locator("#firstName").fill("John")

    # Last Name
    page.locator("#lastName").fill("Doe")

    # Email
    page.locator("#userEmail").fill("john@test.com")

    # Gender: Male — use JS click on label to avoid overlay issues
    page.evaluate("document.querySelector('label[for=gender-radio-1]').click()")

    # Mobile
    page.locator("#userNumber").fill("1234567890")

    # Date of Birth
    page.locator("#dateOfBirthInput").click()
    page.wait_for_timeout(500)
    page.locator(".react-datepicker__year-select").select_option("1990")
    page.locator(".react-datepicker__month-select").select_option("0")  # January
    page.locator(
        ".react-datepicker__day--001:not(.react-datepicker__day--outside-month)"
    ).first.click()

    # Subjects: type then click autocomplete option (Enter would submit the form)
    page.locator("#subjectsInput").fill("Maths")
    page.wait_for_timeout(500)
    page.locator(".subjects-auto-complete__option").first.click()

    # Hobbies: Sports
    page.evaluate("document.querySelector('label[for=hobbies-checkbox-1]').click()")

    # Upload Picture: create a temporary file
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp.write(b"\x89PNG\r\n\x1a\n")
        tmp_path = tmp.name

    try:
        page.locator("#uploadPicture").set_input_files(tmp_path)
    finally:
        os.unlink(tmp_path)

    # Current Address
    page.locator("#currentAddress").fill("123 Test Street")

    # State dropdown (react-select)
    page.locator("#state").click()
    page.wait_for_timeout(300)
    page.locator("#react-select-3-option-0").click()  # NCR

    # City dropdown (react-select)
    page.locator("#city").click()
    page.wait_for_timeout(300)
    page.locator("#react-select-4-option-0").click()  # Delhi

    # Submit
    page.locator("#submit").click()

    # Verify modal appears with submitted values
    modal = page.locator(".modal-content")
    expect(modal).to_be_visible(timeout=10000)
    expect(modal).to_contain_text("Thanks for submitting the form")
    expect(modal).to_contain_text("John Doe")
    expect(modal).to_contain_text("john@test.com")
    expect(modal).to_contain_text("Male")
    expect(modal).to_contain_text("1234567890")
    expect(modal).to_contain_text("Maths")
    expect(modal).to_contain_text("Sports")
    expect(modal).to_contain_text("123 Test Street")
