"""Playwright 테스트 — test_select_old_style (tc_74)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_select_old_style(page):
    """Old style select menu"""
    page.goto(BASE_URL + "/select-menu")
    page.wait_for_load_state("domcontentloaded")

    page.locator("#oldSelectMenu").select_option("3")

    expect(page.locator("#oldSelectMenu")).to_have_value("3", timeout=5000)
