"""Playwright 테스트 — test_selectable_multiple_list (tc_109)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_selectable_multiple_list(page):
    """Selectable multiple list items"""
    page.goto(BASE_URL + "/selectable")
    page.wait_for_load_state("domcontentloaded")

    items = page.locator("#verticalListContainer .list-group-item")
    items.nth(0).click()
    items.nth(1).click()
    items.nth(2).click()
    page.wait_for_timeout(300)

    for i in range(3):
        cls = items.nth(i).get_attribute("class") or ""
        assert "active" in cls, f"Item {i} should be active"
