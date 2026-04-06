from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_challenging_dom_table_read(page: Page):
    page.goto("https://the-internet.herokuapp.com/challenging_dom")
    page.wait_for_load_state("domcontentloaded")

    table = page.locator("table")
    expect(table).to_be_visible(timeout=10000)

    header_row = page.locator("table thead tr")
    expect(header_row).to_be_visible(timeout=5000)

    header_cells = page.locator("table thead tr th")
    header_count = header_cells.count()
    assert header_count > 0, "Expected table headers to exist"

    data_rows = page.locator("table tbody tr")
    row_count = data_rows.count()
    assert row_count > 0, "Expected table data rows to exist"

    first_cell = page.locator("table tbody tr:first-child td:first-child")
    expect(first_cell).to_be_visible(timeout=5000)
    cell_text = first_cell.inner_text()
    assert len(cell_text) > 0, "Expected first cell to have content"
