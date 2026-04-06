"""Playwright 테스트 — test_textbox_only_name (tc_04)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_textbox_only_name(page):
    """Submit text box with only full name"""
    page.goto(BASE_URL + "/text-box")
    page.wait_for_load_state("domcontentloaded")

    page.locator("#userName").fill("Jane Smith")
    page.locator("#submit").scroll_into_view_if_needed()
    page.locator("#submit").click()

    output = page.locator("#output")
    expect(output).to_be_visible(timeout=5000)
    expect(output).to_contain_text("Jane Smith")
