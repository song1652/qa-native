"""Playwright 테스트 — test_sortable_data_table (tc_17)"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_sortable_data_table(page):
    page.goto(BASE_URL + "tables")
    rows = page.locator("#table1 tbody tr")
    expect(rows).to_have_count(4, timeout=5000)
    header = page.locator("#table1 thead th:nth-child(1) span")
    header.click()
    page.wait_for_timeout(500)
    after = []
    for i in range(4):
        after.append(rows.nth(i).locator("td:nth-child(1)").inner_text())
    assert after == sorted(after), f"Expected sorted order, got {after}"
