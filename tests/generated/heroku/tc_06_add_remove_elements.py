"""Playwright 테스트 — test_add_remove_elements (tc_06)"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_add_remove_elements(page):
    page.goto(BASE_URL + "add_remove_elements/")
    add_button = page.locator("button", has_text="Add Element")
    for _ in range(3):
        add_button.click()
    delete_buttons = page.locator(".added-manually")
    expect(delete_buttons).to_have_count(3, timeout=5000)
    delete_buttons.first.click()
    expect(delete_buttons).to_have_count(2, timeout=5000)
