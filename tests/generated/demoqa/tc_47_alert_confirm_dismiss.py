from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"


def test_confirm_alert_dismiss_shows_cancel_message(page: Page):
    page.goto(f"{BASE_URL}/alerts", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    def handle_dialog(dialog):
        dialog.dismiss()

    page.on("dialog", handle_dialog)

    # Click by ID to avoid locator ambiguity
    page.locator("#confirmButton").click()
    page.wait_for_timeout(1000)

    expect(page.locator("#confirmResult")).to_contain_text("Cancel", timeout=5000)
