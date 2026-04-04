import pytest
import json
import re
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_sortable_data_table(page):
    page.goto(BASE_URL + "tables")

    # Verify table1 exists with 4+ rows
    rows = page.locator("#table1 tbody tr")
    expect(rows).to_have_count(4, timeout=10000)

    # Click the SPAN inside the "Last Name" th, not the th itself
    page.locator("#table1 thead th span", has_text="Last Name").click()
    page.wait_for_timeout(500)

    # Read all last name cells (first column)
    last_name_cells = page.locator("#table1 tbody tr td:nth-child(1)")
    count = last_name_cells.count()
    assert count >= 4, f"Expected at least 4 rows, got {count}"

    last_names = [last_name_cells.nth(i).inner_text().strip() for i in range(count)]

    # Verify sorted alphabetically (ascending)
    assert last_names == sorted(last_names), (
        f"Last names not sorted alphabetically. Got: {last_names}"
    )
