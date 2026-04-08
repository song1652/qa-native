from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"

AD_REMOVE_JS = (
    "document.querySelectorAll("
    "'ins.adsbygoogle, iframe[src*=google], iframe[src*=doubleclick]'"
    ").forEach(e => e.remove())"
)


def test_webtable_search_no_results(page):
    page.goto(f"{BASE_URL}/webtables", wait_until="domcontentloaded")
    page.evaluate(AD_REMOVE_JS)
    page.wait_for_timeout(2000)

    # Type non-existent search term into search box
    search_box = page.locator("#searchBox")
    expect(search_box).to_be_visible(timeout=10000)
    search_box.fill("zzzznonexistent")
    page.wait_for_timeout(1000)

    # Verify table shows no matching rows
    # With standard table structure, tbody should have 0 rows or empty rows
    rows = page.locator("table tbody tr")
    row_count = rows.count()

    if row_count > 0:
        # Rows exist but should be empty/no visible data
        all_empty = True
        for i in range(row_count):
            row_text = rows.nth(i).inner_text().strip()
            if row_text:
                all_empty = False
                break
        assert all_empty, f"Expected no results but found row with data: '{rows.first.inner_text().strip()}'"
    # row_count == 0 is also valid (no rows at all)
