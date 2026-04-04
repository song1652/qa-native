"""Playwright 테스트 — test_forgot_password_submit (tc_19)"""
import json
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_forgot_password_submit(page):
    with open(TEST_DATA_PATH, encoding="utf-8") as f:
        data = json.load(f)["heroku"]["forgot_email"]
    page.goto(BASE_URL + "forgot_password")
    email_input = page.locator("#email")
    expect(email_input).to_be_visible(timeout=5000)
    email_input.fill(data["email"])
    page.locator("#form_submit").click()
    page.wait_for_load_state("domcontentloaded")
    expect(page.locator("#email")).not_to_be_visible(timeout=5000)
