from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"


def test_timer_alert_appears_after_5_seconds(page: Page):
    page.goto(f"{BASE_URL}/alerts", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    alert_accepted = []

    def handle_dialog(dialog):
        alert_accepted.append(dialog.message)
        dialog.accept()

    page.on("dialog", handle_dialog)

    # Click by ID to avoid ambiguity with button text
    page.locator("#timerAlertButton").click()
    page.wait_for_timeout(6000)

    assert len(alert_accepted) > 0, "Timer alert did not appear after 5 seconds"
