from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_webtable_add_record(page: Page) -> None:
    page.goto(f"{BASE_URL}/webtables", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    add_btn = page.locator("#addNewRecordButton")
    expect(add_btn).to_be_visible(timeout=10000)
    add_btn.click()

    page.locator("#firstName").fill("Alice")
    page.locator("#lastName").fill("Brown")
    page.locator("#userEmail").fill("alice.brown@example.com")
    page.locator("#age").fill("30")
    page.locator("#salary").fill("50000")
    page.locator("#department").fill("QA")

    page.locator("#submit").click()

    page.wait_for_timeout(1000)

    table = page.locator(".rt-tbody, tbody")
    expect(table).to_contain_text("Alice", timeout=5000)
    expect(table).to_contain_text("Brown", timeout=5000)
    expect(table).to_contain_text("alice.brown@example.com", timeout=5000)
    expect(table).to_contain_text("30", timeout=5000)
    expect(table).to_contain_text("50000", timeout=5000)
    expect(table).to_contain_text("QA", timeout=5000)
