import pytest
import json
import re
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_login_then_logout(page):
    data = json.loads(TEST_DATA_PATH.read_text())["heroku"]
    valid_user = data["valid_user"]

    page.goto(BASE_URL + "login")
    page.fill("#username", valid_user["username"])
    page.fill("#password", valid_user["password"])
    page.click("button[type='submit']")
    page.wait_for_load_state("domcontentloaded")

    page.click("a[href='/logout']")
    page.wait_for_load_state("domcontentloaded")

    expect(page).to_have_url(re.compile(r".*/login"), timeout=10000)
    expect(page.locator("#flash")).to_contain_text("You logged out of the secure area!", timeout=10000)
