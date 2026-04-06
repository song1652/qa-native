"""Playwright 테스트 — test_tabs_more_disabled (tc_113)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tabs_more_disabled(page):
    """Tabs more tab is disabled"""
    page.goto(BASE_URL + "/tabs")
    page.wait_for_load_state("domcontentloaded")

    more_tab = page.locator("#demo-tab-more")
    cls = more_tab.get_attribute("class") or ""
    assert "disabled" in cls, f"More tab should be disabled, got: {cls}"
