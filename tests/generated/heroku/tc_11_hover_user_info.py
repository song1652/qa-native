"""Playwright 테스트 — test_hover_user_info (tc_11)"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_hover_user_info(page):
    page.goto(BASE_URL + "hovers")
    figure = page.locator(".figure").nth(0)
    figure.hover()
    caption = figure.locator(".figcaption")
    expect(caption).to_be_visible(timeout=5000)
    expect(caption.locator("h5")).to_contain_text("name: user1", timeout=5000)
    expect(caption.locator("a")).to_contain_text("View profile", timeout=5000)
