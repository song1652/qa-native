import json
from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_js_prompt_input(page: Page) -> None:
    with open(TEST_DATA_PATH) as f:
        test_data = json.load(f)

    prompt_text = test_data["heroku"]["js_prompt"]["text"]

    page.goto("https://the-internet.herokuapp.com/javascript_alerts")
    page.wait_for_load_state("domcontentloaded")

    def handle_dialog(dialog):
        dialog.accept(prompt_text)

    page.on("dialog", handle_dialog)

    page.get_by_role("button", name="Click for JS Prompt").click()

    expect(page.locator("#result")).to_contain_text(f"You entered: {prompt_text}", timeout=10000)
