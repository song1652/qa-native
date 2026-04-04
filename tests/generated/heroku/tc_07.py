import pytest
import json
import re
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_js_alert(page):
    page.goto(BASE_URL + "javascript_alerts")
    page.on("dialog", lambda dialog: dialog.accept())
    page.get_by_text("Click for JS Alert").click()
    expect(page.locator("#result")).to_contain_text("You successfully clicked an alert", timeout=5000)
