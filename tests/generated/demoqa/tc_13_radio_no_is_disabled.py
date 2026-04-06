"""Playwright 테스트 — test_radio_no_is_disabled (tc_13)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_radio_no_is_disabled(page):
    """Verify No radio button is disabled"""
    page.goto(BASE_URL + "/radio-button")
    page.wait_for_load_state("domcontentloaded")

    no_radio = page.locator("#noRadio")
    expect(no_radio).to_be_disabled(timeout=5000)
