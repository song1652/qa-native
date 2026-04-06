from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_radio_no_is_disabled(page: Page) -> None:
    page.goto(f"{BASE_URL}/radio-button", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    no_radio = page.locator("#noRadio")
    expect(no_radio).to_be_visible(timeout=10000)
    expect(no_radio).to_be_disabled(timeout=5000)

    no_label = page.locator("label[for='noRadio']")
    expect(no_label).to_be_visible(timeout=5000)
    no_label.click(force=True)

    expect(no_radio).not_to_be_checked(timeout=5000)
