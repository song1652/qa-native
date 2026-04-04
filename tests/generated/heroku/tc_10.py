import pytest
import json
import re
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_js_prompt_input(page):
    test_data = json.loads(TEST_DATA_PATH.read_text())["heroku"]
    prompt_text = test_data["js_prompt"]["text"]

    page.on("dialog", lambda dialog: dialog.accept(prompt_text))

    page.goto(BASE_URL + "javascript_alerts")
    page.get_by_text("Click for JS Prompt").click()

    expect(page.locator("#result")).to_contain_text("You entered: Hello Playwright", timeout=10000)
