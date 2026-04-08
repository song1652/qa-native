import json
from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_tooltip_text_field_hover(page: Page):
    page.goto(f"{BASE_URL}/tool-tips", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)
    page.evaluate(
        "document.querySelectorAll('ins.adsbygoogle, iframe[src*=google], iframe[src*=doubleclick], #fixedban, footer').forEach(e => e.remove())"
    )

    # Hover over the text input field
    text_field = page.locator("#toolTipTextField")
    expect(text_field).to_be_visible(timeout=10000)
    text_field.hover()
    page.wait_for_timeout(1000)

    # Verify tooltip text
    tooltip = page.locator(".tooltip-inner")
    expect(tooltip).to_be_visible(timeout=5000)
    expect(tooltip).to_contain_text("You hovered over the text field", timeout=5000)
