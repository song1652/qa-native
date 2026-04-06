import pytest
from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_old_style_select_menu(page: Page):
    page.goto(f"{BASE_URL}/select-menu", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    # Old Style Select Menu is a native <select> element
    old_style_select = page.locator("#oldSelectMenu")
    expect(old_style_select).to_be_visible(timeout=10000)

    old_style_select.select_option(index=1)
    page.wait_for_timeout(500)

    selected_value = old_style_select.evaluate("el => el.options[el.selectedIndex].text")
    assert selected_value, "No option was selected in the old style select menu"
