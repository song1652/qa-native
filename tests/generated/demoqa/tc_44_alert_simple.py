from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"


def test_simple_alert_can_be_accepted(page: Page):
    page.goto(f"{BASE_URL}/alerts", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    alert_accepted = []

    def handle_dialog(dialog):
        alert_accepted.append(dialog.message)
        dialog.accept()

    page.on("dialog", handle_dialog)

    # Click by ID to avoid ambiguity
    page.locator("#alertButton").click()
    page.wait_for_timeout(1000)

    assert len(alert_accepted) > 0, "Alert did not appear"
