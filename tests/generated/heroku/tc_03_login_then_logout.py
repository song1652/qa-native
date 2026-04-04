"""Playwright 테스트 — test_login_then_logout (tc_03)"""
import json
import re
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_login_then_logout(page):
    with open(TEST_DATA_PATH, encoding="utf-8") as f:
        data = json.load(f)["heroku"]["valid_user"]
    page.goto(BASE_URL + "login")
    page.locator("#username").fill(data["username"])
    page.locator("#password").fill(data["password"])
    page.locator("button.radius").click()
    expect(page).to_have_url(re.compile(r"/secure"), timeout=5000)
    page.locator("a[href='/logout']").click()
    page.wait_for_load_state("domcontentloaded")
    expect(page).to_have_url(re.compile(r"/login"), timeout=5000)
    expect(page.locator("#flash")).to_contain_text("You logged out of the secure area!", timeout=5000)
