"""Playwright 테스트 — test_login_invalid_user (tc_02)"""
import json
import re
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_login_invalid_user(page):
    with open(TEST_DATA_PATH, encoding="utf-8") as f:
        data = json.load(f)["heroku"]["invalid_user"]
    page.goto(BASE_URL + "login")
    page.locator("#username").fill(data["username"])
    page.locator("#password").fill(data["password"])
    page.locator("button.radius").click()
    expect(page).to_have_url(re.compile(r"/login"), timeout=5000)
    expect(page.locator("#flash")).to_contain_text("Your username is invalid!", timeout=5000)
