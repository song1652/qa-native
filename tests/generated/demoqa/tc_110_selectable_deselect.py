"""Playwright 테스트 — test_selectable_deselect (tc_110)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_selectable_deselect(page):
    """Selectable deselect item"""
    page.goto(BASE_URL + "/selectable")
    page.wait_for_load_state("domcontentloaded")

    item = page.locator("#verticalListContainer .list-group-item").first
    item.click()
    page.wait_for_timeout(200)
    assert "active" in (item.get_attribute("class") or "")

    item.click()
    page.wait_for_timeout(200)
    assert "active" not in (item.get_attribute("class") or "")
