"""Playwright 테스트 — test_select_multiselect (tc_75)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_select_multiselect(page):
    """Multiselect dropdown"""
    page.goto(BASE_URL + "/select-menu")
    page.wait_for_load_state("domcontentloaded")

    page.locator("#cars").select_option(["volvo", "saab"])

    selected = page.locator("#cars").evaluate(
        "el => Array.from(el.selectedOptions).map(o => o.value)"
    )
    assert "volvo" in selected
    assert "saab" in selected
