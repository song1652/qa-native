"""Playwright 테스트 — test_dynamic_controls_input_enable (tc_13)"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_dynamic_controls_input_enable(page):
    page.goto(BASE_URL + "dynamic_controls")
    text_input = page.locator("#input-example input[type='text']")
    message = page.locator("#message")
    expect(text_input).to_be_disabled(timeout=5000)
    page.locator("#input-example button", has_text="Enable").click()
    expect(message).to_contain_text("It's enabled!", timeout=10000)
    expect(text_input).to_be_enabled(timeout=5000)
