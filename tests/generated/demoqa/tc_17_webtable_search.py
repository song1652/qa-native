from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_webtable_search(page: Page) -> None:
    page.goto(f"{BASE_URL}/webtables", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    search_box = page.locator("#searchBox")
    expect(search_box).to_be_visible(timeout=10000)
    search_box.fill("Cierra")

    page.wait_for_timeout(1000)

    table = page.locator(".rt-tbody, tbody")
    expect(table).to_contain_text("Cierra", timeout=5000)

    rows = page.locator("tbody tr:not(:empty), .rt-tr-group:not(:empty)")
    count = rows.count()
    for i in range(count):
        row_text = rows.nth(i).inner_text()
        if row_text.strip():
            assert "Cierra" in row_text, f"Row {i} does not contain 'Cierra': {row_text}"
