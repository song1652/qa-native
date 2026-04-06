import re
from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_table_sort_web_site(page: Page) -> None:
    page.goto("https://the-internet.herokuapp.com/tables")
    page.wait_for_load_state("domcontentloaded")

    table1 = page.locator("#table1")
    web_site_header = table1.locator("thead th").filter(has_text="Web Site")
    web_site_header.click()
    page.wait_for_timeout(300)

    expect(web_site_header).to_have_class(re.compile(r"headerSortDown|headerSortUp"), timeout=5000)
