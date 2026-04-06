"""Playwright 테스트 — test_selectable_list (tc_79)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_selectable_list(page):
    """Selectable list item"""
    page.goto(BASE_URL + "/selectable")
    page.wait_for_load_state("domcontentloaded")

    item = page.locator("#verticalListContainer .list-group-item").first
    item.click()
    page.wait_for_timeout(300)

    cls = item.get_attribute("class") or ""
    assert "active" in cls, f"Item should be active, got: {cls}"
