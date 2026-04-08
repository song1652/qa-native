from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"


def test_modal_large_opens_and_can_be_closed(page: Page):
    page.goto(f"{BASE_URL}/modal-dialogs")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(2000)

    # Remove ads/overlays
    page.evaluate(
        "document.querySelectorAll('ins.adsbygoogle, iframe[src*=google], "
        "iframe[src*=doubleclick], #fixedban, footer').forEach(e => e.remove())"
    )

    # Click Large Modal button
    page.get_by_role("button", name="Large Modal").click()

    # Verify modal is visible
    modal = page.locator(".modal-dialog")
    expect(modal).to_be_visible(timeout=10000)

    # Verify modal body has content (long text)
    modal_body = page.locator(".modal-body")
    expect(modal_body).to_be_visible(timeout=5000)

    modal_text = modal_body.inner_text()
    assert len(modal_text) > 50, f"Expected long modal text, got: {modal_text!r}"

    # Close using the specific close button - use ID to avoid strict mode violation
    page.locator("#closeLargeModal").click()

    # Verify modal is gone
    expect(modal).to_be_hidden(timeout=5000)
