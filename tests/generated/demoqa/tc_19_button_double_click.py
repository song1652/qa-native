from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_button_double_click(page: Page) -> None:
    page.goto(f"{BASE_URL}/buttons", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    double_click_btn = page.locator("#doubleClickBtn")
    expect(double_click_btn).to_be_visible(timeout=10000)
    double_click_btn.dblclick()

    result = page.locator("#doubleClickMessage")
    expect(result).to_be_visible(timeout=5000)
    expect(result).to_contain_text("double click", timeout=5000)
