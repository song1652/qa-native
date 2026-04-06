"""Playwright 테스트 — test_radio_select_yes (tc_11)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_radio_select_yes(page):
    """Select Yes radio button"""
    page.goto(BASE_URL + "/radio-button")
    page.wait_for_load_state("domcontentloaded")

    page.locator("label[for='yesRadio']").click()

    expect(page.locator(".text-success")).to_contain_text("Yes", timeout=5000)
