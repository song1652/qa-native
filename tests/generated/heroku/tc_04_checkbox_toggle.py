"""Playwright 테스트 — test_checkbox_toggle (tc_04)"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_checkbox_toggle(page):
    page.goto(BASE_URL + "checkboxes")
    checkboxes = page.locator("#checkboxes input[type='checkbox']")
    checkboxes.nth(0).click()
    checkboxes.nth(1).click()
    expect(checkboxes.nth(0)).to_be_checked()
    expect(checkboxes.nth(1)).not_to_be_checked()
