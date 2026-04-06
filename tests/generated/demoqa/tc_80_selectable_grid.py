"""Playwright 테스트 — test_selectable_grid (tc_80)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_selectable_grid(page):
    """Selectable grid item"""
    page.goto(BASE_URL + "/selectable")
    page.wait_for_load_state("domcontentloaded")

    page.locator("#demo-tab-grid").click()
    page.wait_for_timeout(300)

    item = page.locator("#gridContainer .list-group-item").first
    item.click()
    page.wait_for_timeout(300)

    cls = item.get_attribute("class") or ""
    assert "active" in cls, f"Grid item should be active, got: {cls}"
