import pytest
from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_menu_main_items_display(page: Page):
    page.goto(f"{BASE_URL}/menu", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    item1 = page.get_by_text("Main Item 1", exact=True)
    item2 = page.get_by_text("Main Item 2", exact=True)
    item3 = page.get_by_text("Main Item 3", exact=True)

    expect(item1).to_be_visible(timeout=10000)
    expect(item2).to_be_visible(timeout=10000)
    expect(item3).to_be_visible(timeout=10000)
