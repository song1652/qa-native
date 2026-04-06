from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_multiselect_dropdown(page: Page):
    page.goto(f"{BASE_URL}/select-menu", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    # #cars is a standard HTML <select multiple> element (not react-select)
    cars_select = page.locator("#cars")
    expect(cars_select).to_be_visible(timeout=10000)

    # Select multiple options using standard select_option
    cars_select.select_option(["volvo", "saab"])
    page.wait_for_timeout(300)

    # Verify selected values
    selected_values = page.evaluate("Array.from(document.querySelector('#cars').selectedOptions).map(o => o.value)")
    assert "volvo" in selected_values, f"Expected 'volvo' to be selected, got: {selected_values}"
    assert "saab" in selected_values, f"Expected 'saab' to be selected, got: {selected_values}"
    assert len(selected_values) >= 2, f"Expected at least 2 selected, got: {selected_values}"
