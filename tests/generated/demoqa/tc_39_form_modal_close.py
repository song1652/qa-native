from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"

AD_REMOVE_JS = (
    "document.querySelectorAll("
    "'ins.adsbygoogle, iframe[src*=google], iframe[src*=doubleclick], #fixedban, footer'"
    ").forEach(e => e.remove())"
)


def test_form_modal_close_after_submit(page: Page):
    page.goto(f"{BASE_URL}/automation-practice-form")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(2000)

    page.evaluate(AD_REMOVE_JS)

    page.locator("#firstName").fill("John")
    page.locator("#lastName").fill("Doe")

    # Select Male gender
    page.locator("label[for='gender-radio-1']").click()

    page.locator("#userNumber").fill("1234567890")

    # Scroll to and click Submit
    submit_btn = page.locator("#submit")
    submit_btn.scroll_into_view_if_needed()
    submit_btn.click()

    # Wait for modal to appear
    modal_title = page.locator("#example-modal-sizes-title-lg")
    expect(modal_title).to_be_visible(timeout=10000)

    # Close modal using Escape key (closeLargeModal button doesn't work reliably)
    page.keyboard.press("Escape")
    page.wait_for_timeout(1000)

    # Modal should be hidden
    expect(modal_title).to_be_hidden(timeout=5000)

    # Should still be on the form page
    expect(page).to_have_url(f"{BASE_URL}/automation-practice-form")
