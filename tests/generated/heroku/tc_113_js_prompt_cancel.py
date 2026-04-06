import json
from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_js_prompt_cancel(page: Page):
    """TC-113: JS Prompt 취소 - 결과 텍스트에 'You entered: null' 표시"""
    page.goto("https://the-internet.herokuapp.com/javascript_alerts")
    page.wait_for_load_state("domcontentloaded")

    dialog_messages = []

    def handle_dialog(dialog):
        dialog_messages.append(dialog.message)
        dialog.dismiss()

    page.on("dialog", handle_dialog)

    page.get_by_role("button", name="Click for JS Prompt").click()

    result = page.locator("#result")
    expect(result).to_contain_text("You entered: null", timeout=10000)
