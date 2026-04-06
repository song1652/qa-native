from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_webtable_edit_record(page: Page) -> None:
    page.goto(f"{BASE_URL}/webtables", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    edit_btn = page.locator("[id^='edit-record-']").first
    expect(edit_btn).to_be_visible(timeout=10000)
    edit_btn.click()

    first_name_field = page.locator("#firstName")
    expect(first_name_field).to_be_visible(timeout=5000)
    first_name_field.click(click_count=3)
    first_name_field.fill("UpdatedName")

    page.locator("#submit").click()

    page.wait_for_timeout(1000)

    table = page.locator(".rt-tbody, tbody")
    expect(table).to_contain_text("UpdatedName", timeout=5000)
