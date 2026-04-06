"""Playwright 테스트 — test_webtable_delete_record (tc_16)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_webtable_delete_record(page):
    """Delete a record from web table"""
    page.goto(BASE_URL + "/webtables")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(1000)

    first_name = page.locator("table tbody tr:first-child td:first-child").inner_text()
    assert first_name.strip() != "", "First record should have a name"

    page.locator("#delete-record-1").click()
    page.wait_for_timeout(500)

    new_first = page.locator("table tbody tr:first-child td:first-child").inner_text()
    assert new_first != first_name, f"First record should change after delete"
