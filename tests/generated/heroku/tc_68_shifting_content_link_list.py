import pytest
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_shifting_content_link_list(page: Page):
    page.goto("https://the-internet.herokuapp.com/shifting_content")
    page.wait_for_load_state("domcontentloaded")

    expect(page.get_by_role("link", name="Example 1: Menu Element")).to_be_visible(timeout=10000)
    expect(page.get_by_role("link", name="Example 2: An image")).to_be_visible(timeout=10000)
    expect(page.get_by_role("link", name="Example 3: List")).to_be_visible(timeout=10000)
