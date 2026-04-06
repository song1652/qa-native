"""Playwright 테스트 — test_textbox_long_address (tc_05)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_textbox_long_address(page):
    """Submit text box with long current address"""
    page.goto(BASE_URL + "/text-box")
    page.wait_for_load_state("domcontentloaded")

    long_addr = "A" * 300
    page.locator("#currentAddress").fill(long_addr)
    page.locator("#submit").scroll_into_view_if_needed()
    page.locator("#submit").click()

    output = page.locator("#output")
    expect(output).to_be_visible(timeout=5000)
    expect(output).to_contain_text(long_addr[:50])
