"""Playwright 테스트 — test_webtable_search_no_results (tc_106)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_webtable_search_no_results(page):
    """Web table search no results"""
    page.goto(BASE_URL + "/webtables")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(1000)

    page.locator("#searchBox").fill("zzzznonexistent")
    page.wait_for_timeout(500)

    # Table body should have no data rows (rows with empty cells only)
    rows = page.locator("table tbody tr")
    visible_data = False
    for i in range(rows.count()):
        first_cell = rows.nth(i).locator("td:first-child").inner_text().strip()
        if first_cell and first_cell != "":
            visible_data = True
            break
    assert not visible_data, "No matching rows should be visible"
