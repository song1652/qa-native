"""Playwright 테스트 — test_textbox_empty_submit (tc_02)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_textbox_empty_submit(page):
    """Submit text box with no input"""
    page.goto(BASE_URL + "/text-box")
    page.wait_for_load_state("domcontentloaded")

    page.locator("#submit").scroll_into_view_if_needed()
    page.locator("#submit").click()
    page.wait_for_timeout(500)

    # Output should not show or be empty
    output = page.locator("#output")
    assert output.locator("p").count() == 0, "No output paragraphs expected"
