"""Playwright 테스트 — test_js_confirm_dismiss (tc_09)"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_js_confirm_dismiss(page):
    page.goto(BASE_URL + "javascript_alerts")
    page.on("dialog", lambda dialog: dialog.dismiss())
    page.locator("button", has_text="Click for JS Confirm").click()
    expect(page.locator("#result")).to_contain_text("You clicked: Cancel", timeout=5000)
