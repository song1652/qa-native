import json
import re
from pathlib import Path

import pytest
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_login_failure_invalid_user(page):
    test_data = json.loads(TEST_DATA_PATH.read_text())["heroku"]
    invalid_user = test_data["invalid_user"]

    page.goto(BASE_URL + "login")
    page.fill("#username", invalid_user["username"])
    page.fill("#password", invalid_user["password"])
    page.click("button[type='submit']")

    expect(page).to_have_url(re.compile(r".*/login"))
    expect(page.locator("#flash")).to_contain_text("Your username is invalid!", timeout=5000)
