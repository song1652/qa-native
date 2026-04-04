"""Playwright 테스트 — test_number_input (tc_20)"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_number_input(page):
    page.goto(BASE_URL + "inputs")
    number_input = page.locator("input[type='number']")
    number_input.fill("42")
    expect(number_input).to_have_value("42", timeout=5000)
    expect(number_input).to_have_attribute("type", "number", timeout=5000)
