"""Playwright 테스트 — test_button_dynamic_click (tc_21)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_button_dynamic_click(page):
    """Dynamic click button"""
    page.goto(BASE_URL + "/buttons")
    page.wait_for_load_state("domcontentloaded")

    # Third button has dynamic ID; use text selector excluding double/right click
    buttons = page.locator("button:has-text('Click Me')")
    # The dynamic click button is the last one that says exactly "Click Me"
    for i in range(buttons.count()):
        text = buttons.nth(i).inner_text()
        if text.strip() == "Click Me":
            buttons.nth(i).click()
            break

    expect(page.locator("#dynamicClickMessage")).to_contain_text(
        "You have done a dynamic click", timeout=5000
    )
