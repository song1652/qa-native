"""Playwright 테스트 — test_button_right_click (tc_20)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_button_right_click(page):
    """Right click button"""
    page.goto(BASE_URL + "/buttons")
    page.wait_for_load_state("domcontentloaded")

    page.locator("#rightClickBtn").click(button="right")

    expect(page.locator("#rightClickMessage")).to_contain_text(
        "You have done a right click", timeout=5000
    )
