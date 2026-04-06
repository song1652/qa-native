from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"


def test_prompt_alert_accepts_input_and_displays_it(page: Page):
    page.goto(f"{BASE_URL}/alerts", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    def handle_dialog(dialog):
        dialog.accept("TestUser")

    page.on("dialog", handle_dialog)

    # Click by ID to avoid locator ambiguity
    page.locator("#promtButton").click()
    page.wait_for_timeout(1000)

    expect(page.locator("#promptResult")).to_contain_text("TestUser", timeout=5000)
