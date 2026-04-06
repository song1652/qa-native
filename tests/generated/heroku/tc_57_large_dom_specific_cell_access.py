from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = (
    Path(__file__).resolve()
    .parent.parent.parent.parent
    / "config" / "test_data.json"
)


def test_large_dom_specific_cell_access(page: Page):
    """대규모 DOM 특정 요소 접근"""
    page.goto("https://the-internet.herokuapp.com/large")
    page.wait_for_load_state("domcontentloaded")

    table = page.locator("table")
    expect(table.first).to_be_visible(timeout=10000)

    row_50_cell_1 = page.locator("table tr:nth-child(50) td:nth-child(1)")
    expect(row_50_cell_1).to_be_visible(timeout=10000)

    cell_text = row_50_cell_1.inner_text()
    assert "50.1" in cell_text, (
        f"Expected '50.1' in cell text, got: '{cell_text}'"
    )
