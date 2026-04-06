"""Playwright 테스트 — test_select_one (tc_73)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_select_one(page):
    """Select one dropdown"""
    page.goto(BASE_URL + "/select-menu")
    page.wait_for_load_state("domcontentloaded")

    page.locator("#selectOne").click()
    page.locator("#selectOne input").fill("Mrs.")
    page.locator("#selectOne input").press("Enter")

    expect(page.locator("#selectOne")).to_contain_text("Mrs.", timeout=5000)
