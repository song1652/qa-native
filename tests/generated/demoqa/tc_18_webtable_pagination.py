"""Playwright 테스트 — test_webtable_pagination (tc_18)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_webtable_pagination(page):
    """Change rows per page in web table"""
    page.goto(BASE_URL + "/webtables")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(1000)

    rows_select = page.locator("select.form-control")
    expect(rows_select).to_be_visible(timeout=5000)

    rows_select.select_option("10")
    page.wait_for_timeout(500)
    expect(rows_select).to_have_value("10")
