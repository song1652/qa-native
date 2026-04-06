"""Playwright 테스트 — test_textbox_fill_all_fields (tc_01)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_textbox_fill_all_fields(page):
    """Fill all text box fields and submit"""
    page.goto(BASE_URL + "/text-box")
    page.wait_for_load_state("domcontentloaded")

    page.locator("#userName").fill("John Doe")
    page.locator("#userEmail").fill("john.doe@example.com")
    page.locator("#currentAddress").fill("123 Main St, Springfield")
    page.locator("#permanentAddress").fill("456 Oak Ave, Shelbyville")

    page.locator("#submit").scroll_into_view_if_needed()
    page.locator("#submit").click()

    output = page.locator("#output")
    expect(output).to_be_visible(timeout=5000)
    expect(output).to_contain_text("John Doe")
    expect(output).to_contain_text("john.doe@example.com")
    expect(output).to_contain_text("123 Main St, Springfield")
    expect(output).to_contain_text("456 Oak Ave, Shelbyville")
