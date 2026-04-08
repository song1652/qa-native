from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_webtable_delete_record(page: Page) -> None:
    page.goto(f"{BASE_URL}/webtables", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    first_row = page.locator("tbody tr, .rt-tr-group").first
    expect(first_row).to_be_visible(timeout=10000)
    first_name_cell = first_row.locator("td, .rt-td").first
    first_name_text = first_name_cell.inner_text()

    delete_btn = page.locator("[id^='delete-record-']").first
    expect(delete_btn).to_be_visible(timeout=5000)
    delete_btn.click()

    page.wait_for_timeout(1000)

    table = page.locator(".rt-tbody, tbody")
    if first_name_text.strip():
        expect(table).not_to_contain_text(first_name_text.strip(), timeout=5000)
