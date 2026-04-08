from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"


def test_modal_small_opens_and_can_be_closed(page: Page):
    page.goto(f"{BASE_URL}/modal-dialogs")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(2000)

    # Remove ads/overlays
    page.evaluate(
        "document.querySelectorAll('ins.adsbygoogle, iframe[src*=google], "
        "iframe[src*=doubleclick], #fixedban, footer').forEach(e => e.remove())"
    )

    # Click Small Modal button
    page.get_by_role("button", name="Small Modal").click()

    # Verify modal is visible with expected text
    modal = page.locator(".modal-dialog")
    expect(modal).to_be_visible(timeout=10000)
    expect(modal).to_contain_text("This is a small modal")

    # Close using the specific close button (not the x button)
    # Use ID to avoid strict mode violation between btn-close (x) and Close button
    page.locator("#closeSmallModal").click()

    # Verify modal is gone
    expect(modal).to_be_hidden(timeout=5000)
