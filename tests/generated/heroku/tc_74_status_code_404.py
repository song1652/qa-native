import pytest
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_status_code_404(page: Page):
    page.goto("https://the-internet.herokuapp.com/status_codes")
    page.wait_for_load_state("domcontentloaded")

    page.get_by_role("link", name="404").click()
    page.wait_for_load_state("domcontentloaded")

    expect(page.locator("body")).to_contain_text("404", timeout=10000)
    expect(page.locator("body")).to_contain_text("This page returned a 404 status code", timeout=10000)
