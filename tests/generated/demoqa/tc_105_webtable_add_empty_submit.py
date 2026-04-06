"""Playwright 테스트 — test_webtable_add_empty_submit (tc_105)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_webtable_add_empty_submit(page):
    """Web table add empty submit validation"""
    page.goto(BASE_URL + "/webtables")
    page.wait_for_load_state("domcontentloaded")

    page.locator("#addNewRecordButton").click()
    page.locator("#submit").click()
    page.wait_for_timeout(500)

    # Form should still be visible (not closed)
    expect(page.locator("#registration-form-modal")).to_be_visible(timeout=3000)
