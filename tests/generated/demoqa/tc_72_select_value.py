"""Playwright 테스트 — test_select_value (tc_72)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_select_value(page):
    """Select value dropdown"""
    page.goto(BASE_URL + "/select-menu")
    page.wait_for_load_state("domcontentloaded")

    page.locator("#withOptGroup").click()
    page.locator("#withOptGroup input").fill("Group 1")
    page.locator("#withOptGroup input").press("Enter")

    expect(page.locator("#withOptGroup")).to_contain_text("Group 1", timeout=5000)
