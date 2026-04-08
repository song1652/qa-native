from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"

AD_REMOVE_JS = (
    "document.querySelectorAll("
    "'ins.adsbygoogle, iframe[src*=google], iframe[src*=doubleclick], #fixedban, footer'"
    ").forEach(e => e.remove())"
)


def test_form_invalid_mobile(page: Page):
    page.goto(f"{BASE_URL}/automation-practice-form")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(2000)

    page.evaluate(AD_REMOVE_JS)

    page.locator("#firstName").fill("John")
    page.locator("#lastName").fill("Doe")

    # Select Male gender
    page.locator("label[for='gender-radio-1']").click()

    # Enter non-numeric mobile value
    page.locator("#userNumber").fill("abc")

    # Scroll to and click Submit
    submit_btn = page.locator("#submit")
    submit_btn.scroll_into_view_if_needed()
    submit_btn.click()
    page.wait_for_timeout(1000)

    # Verify modal did NOT appear
    expect(page.locator("#example-modal-sizes-title-lg")).to_be_hidden(timeout=3000)

    # Mobile field should show validation error styling
    mobile_field = page.locator("#userNumber")
    has_error = mobile_field.evaluate(
        "el => {"
        "  const cls = el.className;"
        "  const bc = window.getComputedStyle(el).borderColor;"
        "  return cls.includes('field-error') || cls.includes('is-invalid')"
        "    || bc.includes('255, 0, 0') || bc.includes('220, 53, 69');"
        "}"
    )
    assert has_error, "Mobile field should show validation error styling"
