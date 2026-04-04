"""Playwright 테스트 — test_key_press_detection (tc_14)"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_key_press_detection(page):
    page.goto(BASE_URL + "key_presses")
    page.locator("#target").click()
    page.locator("#target").press("a")
    expect(page.locator("#result")).to_contain_text("You entered: A", timeout=5000)
