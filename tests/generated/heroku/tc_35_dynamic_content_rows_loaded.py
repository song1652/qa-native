from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_dynamic_content_rows_loaded(page: Page) -> None:
    page.goto("https://the-internet.herokuapp.com/dynamic_content")
    page.wait_for_load_state("domcontentloaded")

    # row 0 is the layout header row; rows 1-3 are actual content rows
    rows = page.locator("#content .row")
    row_count = rows.count()
    assert row_count >= 2, f"Expected at least 2 rows (header + content), got {row_count}"

    content_row_found = False
    for i in range(1, row_count):
        row = rows.nth(i)
        imgs = row.locator("img")
        divs = row.locator("div")
        if imgs.count() == 1 and divs.count() >= 2:
            expect(imgs.first).to_be_visible(timeout=5000)
            expect(divs.nth(1)).to_be_visible(timeout=5000)
            content_row_found = True

    assert content_row_found, "No valid content rows found"
