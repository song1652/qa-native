import json
from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_js_confirm_cancel(page: Page) -> None:
    page.goto("https://the-internet.herokuapp.com/javascript_alerts")
    page.wait_for_load_state("domcontentloaded")

    dialog_message = []

    def handle_dialog(dialog):
        dialog_message.append(dialog.message)
        dialog.dismiss()

    page.on("dialog", handle_dialog)

    page.get_by_role("button", name="Click for JS Confirm").click()

    expect(page.locator("#result")).to_contain_text("You clicked: Cancel", timeout=10000)
