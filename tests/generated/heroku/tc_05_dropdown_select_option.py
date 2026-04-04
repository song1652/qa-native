"""Playwright 테스트 — test_dropdown_select_option (tc_05)"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_dropdown_select_option(page):
    page.goto(BASE_URL + "dropdown")
    dropdown = page.locator("#dropdown")
    dropdown.select_option("1")
    expect(dropdown).to_have_value("1", timeout=5000)
    dropdown.select_option("2")
    expect(dropdown).to_have_value("2", timeout=5000)
