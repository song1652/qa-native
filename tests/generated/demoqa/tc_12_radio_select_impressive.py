from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_radio_select_impressive(page: Page) -> None:
    page.goto(f"{BASE_URL}/radio-button", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    impressive_label = page.locator("label[for='impressiveRadio']")
    expect(impressive_label).to_be_visible(timeout=10000)
    impressive_label.click()

    radio = page.locator("#impressiveRadio")
    expect(radio).to_be_checked(timeout=5000)

    result = page.locator(".mt-3")
    expect(result).to_contain_text("Impressive", timeout=5000)
