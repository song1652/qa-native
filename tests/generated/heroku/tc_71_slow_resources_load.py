import pytest
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_slow_resources_load(page: Page):
    page.goto("https://the-internet.herokuapp.com/slow", timeout=30000)
    page.wait_for_load_state("domcontentloaded", timeout=30000)

    heading = page.get_by_role("heading", name="Slow Resources")
    expect(heading).to_be_visible(timeout=30000)
