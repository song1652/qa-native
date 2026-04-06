"""Playwright 테스트 — test_webtable_add_record (tc_14)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_webtable_add_record(page):
    """Add new record to web table"""
    page.goto(BASE_URL + "/webtables")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(1000)

    page.locator("#addNewRecordButton").click()
    page.wait_for_timeout(500)
    page.locator("#firstName").fill("Alice")
    page.locator("#lastName").fill("Brown")
    page.locator("#userEmail").fill("alice.brown@example.com")
    page.locator("#age").fill("30")
    page.locator("#salary").fill("50000")
    page.locator("#department").fill("QA")
    page.locator("#submit").click()
    page.wait_for_timeout(500)

    expect(page.locator("table tbody")).to_contain_text("Alice", timeout=5000)
    expect(page.locator("table tbody")).to_contain_text("Brown", timeout=5000)
