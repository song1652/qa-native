import pytest
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_status_code_200(page: Page):
    page.goto("https://the-internet.herokuapp.com/status_codes")
    page.wait_for_load_state("domcontentloaded")

    page.get_by_role("link", name="200").click()
    page.wait_for_load_state("domcontentloaded")

    expect(page.locator("body")).to_contain_text("200", timeout=10000)
    expect(page.locator("body")).to_contain_text("This page returned a 200 status code", timeout=10000)
