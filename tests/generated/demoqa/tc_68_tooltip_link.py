import pytest
from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_tooltip_contrary_link_hover(page: Page):
    page.goto(f"{BASE_URL}/tool-tips", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    contrary_link = page.get_by_text("Contrary", exact=True)
    expect(contrary_link).to_be_visible(timeout=10000)
    contrary_link.hover()

    tooltip = page.locator(".tooltip-inner")
    expect(tooltip).to_be_visible(timeout=10000)
    expect(tooltip).to_contain_text("You hovered over the Contrary", timeout=10000)
