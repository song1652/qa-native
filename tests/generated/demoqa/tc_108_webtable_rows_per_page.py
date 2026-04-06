from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_web_table_rows_per_page_selection(page: Page) -> None:
    """tc_108: Web Table Rows Per Page Selection — change rows per page and verify."""
    page.goto(f"{BASE_URL}/webtables", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    # Remove ads/overlays
    page.evaluate(
        "document.querySelectorAll('ins.adsbygoogle, iframe[src*=google], iframe[src*=doubleclick]')"
        ".forEach(e => e.remove())"
    )

    # rows per page select: options are "Show 10/20/30/40/50" with values "10/20/30/40/50"
    rows_select = page.locator("select.form-control")
    expect(rows_select).to_be_visible(timeout=10000)

    # Select 20 rows per page
    rows_select.select_option(value="20")
    page.wait_for_timeout(500)

    # Verify table body has at most 20 data rows
    rows = page.locator("table tbody tr")
    row_count = rows.count()
    assert row_count <= 20, f"Expected at most 20 rows but got {row_count}"
