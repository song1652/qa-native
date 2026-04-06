"""Playwright 테스트 — test_tabs_switch (tc_65)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tabs_switch(page):
    """Tabs switch content on click"""
    page.goto(BASE_URL + "/tabs")
    page.wait_for_load_state("domcontentloaded")

    page.locator("#demo-tab-origin").click()
    expect(page.locator("#demo-tabpane-origin")).to_be_visible(timeout=5000)

    page.locator("#demo-tab-use").click()
    expect(page.locator("#demo-tabpane-use")).to_be_visible(timeout=5000)
