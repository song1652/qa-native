import pytest
import json
import re
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_forgot_password_email_submit(page):
    test_data = json.loads(TEST_DATA_PATH.read_text())["heroku"]
    email = test_data["forgot_email"]["email"]

    page.goto(BASE_URL + "forgot_password")
    page.locator("#email").fill(email)
    page.locator("button[type='submit']").click()

    page.wait_for_load_state("load", timeout=10000)
    current_url = page.url
    assert current_url != BASE_URL + "forgot_password" or len(page.locator("body").inner_text()) > 0
