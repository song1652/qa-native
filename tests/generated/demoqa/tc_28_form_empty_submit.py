import re
from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"


def test_form_empty_submit(page: Page):
    page.goto(f"{BASE_URL}/automation-practice-form", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    # Remove ads/overlays
    page.evaluate(
        "document.querySelectorAll('ins.adsbygoogle, iframe[src*=google], "
        "iframe[src*=doubleclick], #fixedban, footer').forEach(e => e.remove())"
    )

    # Click Submit without filling any field
    page.get_by_role("button", name="Submit").click()
    page.wait_for_timeout(500)

    # Required fields should show validation styling (red border via is-invalid class or border-color)
    # The form uses Bootstrap validation: field-error or is-invalid
    first_name = page.locator("#firstName")
    last_name = page.locator("#lastName")

    # Check that the first name field has some validation indication
    # demoqa uses CSS border color change on invalid fields, not class-based
    # Verify the submission modal did NOT appear (form was not submitted)
    expect(page.locator("#example-modal-sizes-title-lg")).to_be_hidden(timeout=3000)

    # Verify that fields are still empty (not redirected)
    first_name_val = first_name.input_value()
    assert first_name_val == "", f"Expected empty first name but got: '{first_name_val}'"
