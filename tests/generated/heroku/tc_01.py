import pytest
import json
import re
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_login_success(page):
    test_data = json.loads(TEST_DATA_PATH.read_text())["heroku"]
    username = test_data["valid_user"]["username"]
    password = test_data["valid_user"]["password"]

    page.goto(BASE_URL + "login")

    page.locator("#username").fill(username)
    page.locator("#password").fill(password)
    page.locator("button[type='submit']").click()

    expect(page).to_have_url(re.compile(r".*/secure"))
    expect(page.locator("#flash")).to_contain_text("You logged into a secure area!", timeout=10000)
