from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_select_value_dropdown(page: Page):
    page.goto(f"{BASE_URL}/select-menu", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    # "Select Value" react-select: click the control, then pick an option
    select_value_container = page.locator("#withOptGroup")
    expect(select_value_container).to_be_visible(timeout=10000)
    select_value_container.click()
    page.wait_for_timeout(500)

    # Options use dynamic CSS class names - find by role
    option = page.get_by_role("option").first
    expect(option).to_be_visible(timeout=10000)
    option_text = option.inner_text()
    option.click()
    page.wait_for_timeout(500)

    # Verify selected value is displayed in the container
    selected_text = page.evaluate(
        "document.querySelector('#withOptGroup [class*=\"singleValue\"], "
        "#withOptGroup [class*=\"single-value\"]')?.textContent"
    )
    assert selected_text is not None, "No selected value found in #withOptGroup"
    assert option_text in selected_text, f"Expected '{option_text}' in selected value, got '{selected_text}'"
