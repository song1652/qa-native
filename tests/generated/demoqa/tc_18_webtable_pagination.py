from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_webtable_pagination(page: Page) -> None:
    page.goto(f"{BASE_URL}/webtables", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    rows_select = page.locator("select.form-control")
    expect(rows_select).to_be_visible(timeout=10000)

    # Select 10 rows per page (minimum available, options: 10/20/30/40/50)
    rows_select.select_option(value="10")
    page.wait_for_timeout(1000)

    visible_rows_10 = page.locator("tbody tr").count()
    assert visible_rows_10 <= 10, f"Expected at most 10 rows but got {visible_rows_10}"

    # Select 20 rows per page
    rows_select.select_option(value="20")
    page.wait_for_timeout(1000)

    visible_rows_20 = page.locator("tbody tr").count()
    assert visible_rows_20 <= 20, f"Expected at most 20 rows but got {visible_rows_20}"
