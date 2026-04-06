"""Playwright 테스트 — test_sortable_tab_switch (tc_78)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_sortable_tab_switch(page):
    """Sortable tab switch"""
    page.goto(BASE_URL + "/sortable")
    page.wait_for_load_state("domcontentloaded")

    expect(page.locator(".vertical-list-container")).to_be_visible(timeout=5000)

    page.locator("#demo-tab-grid").click()
    expect(page.locator(".create-grid")).to_be_visible(timeout=5000)
