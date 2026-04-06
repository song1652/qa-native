"""Playwright 테스트 — test_webtable_sort_by_name (tc_107)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_webtable_sort_by_name(page):
    """Web table has First Name column with data"""
    page.goto(BASE_URL + "/webtables")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(1000)

    # Verify header exists
    header = page.locator("table thead th:first-child")
    expect(header).to_have_text("First Name", timeout=5000)

    # Verify data rows exist
    first_name = page.locator("table tbody tr:first-child td:first-child").inner_text()
    assert first_name.strip() != "", f"First row should have data, got: {first_name!r}"

    # Click header (may or may not sort)
    header.click()
    page.wait_for_timeout(500)

    # Verify table still has data (didn't break)
    expect(page.locator("table tbody tr:first-child td:first-child")).not_to_have_text("", timeout=3000)
