"""Playwright 테스트 — test_dynamic_controls_checkbox_remove_add (tc_12)"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_dynamic_controls_checkbox_remove_add(page):
    page.goto(BASE_URL + "dynamic_controls")
    checkbox = page.locator("#checkbox-example input[type='checkbox']")
    message = page.locator("#message")
    page.locator("button", has_text="Remove").click()
    expect(message).to_contain_text("It's gone!", timeout=10000)
    expect(checkbox).to_have_count(0, timeout=5000)
    page.locator("button", has_text="Add").click()
    expect(message).to_contain_text("It's back!", timeout=10000)
    expect(page.locator("#checkbox-example input[type='checkbox']")).to_have_count(1, timeout=5000)
