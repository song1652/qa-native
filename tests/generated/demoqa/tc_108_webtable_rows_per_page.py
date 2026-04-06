"""Playwright 테스트 — test_webtable_rows_per_page (tc_108)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_webtable_rows_per_page(page):
    """Change rows per page selection"""
    page.goto(BASE_URL + "/webtables")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(1000)

    rows_select = page.locator("select.form-control")
    expect(rows_select).to_be_visible(timeout=5000)

    # demoqa webtables uses Show 10/20/30/40/50 options
    rows_select.select_option("20")
    page.wait_for_timeout(500)
    expect(rows_select).to_have_value("20")
