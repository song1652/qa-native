"""Playwright 테스트 — test_webtable_edit_record (tc_15)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_webtable_edit_record(page):
    """Edit existing record in web table"""
    page.goto(BASE_URL + "/webtables")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(1000)

    page.locator("#edit-record-1").click()
    page.wait_for_timeout(500)
    page.locator("#firstName").clear()
    page.locator("#firstName").fill("UpdatedName")
    page.locator("#submit").click()
    page.wait_for_timeout(500)

    expect(page.locator("table tbody")).to_contain_text("UpdatedName", timeout=5000)
