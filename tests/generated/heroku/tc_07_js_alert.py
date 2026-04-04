"""Playwright 테스트 — test_js_alert (tc_07)"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_js_alert(page):
    page.goto(BASE_URL + "javascript_alerts")
    page.on("dialog", lambda dialog: dialog.accept())
    page.locator("button", has_text="Click for JS Alert").click()
    expect(page.locator("#result")).to_contain_text("You successfully clicked an alert", timeout=5000)
