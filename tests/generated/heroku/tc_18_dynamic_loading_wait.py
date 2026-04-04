"""Playwright 테스트 — test_dynamic_loading_wait (tc_18)"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_dynamic_loading_wait(page):
    page.goto(BASE_URL + "dynamic_loading/1")
    page.locator("button", has_text="Start").click()
    expect(page.locator("#finish")).to_be_visible(timeout=15000)
    expect(page.locator("#finish")).to_contain_text("Hello World!", timeout=5000)
