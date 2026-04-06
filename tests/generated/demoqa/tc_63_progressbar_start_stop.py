"""Playwright 테스트 — test_progressbar_start_stop (tc_63)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_progressbar_start_stop(page):
    """Progress bar starts and stops"""
    page.goto(BASE_URL + "/progress-bar")
    page.wait_for_load_state("domcontentloaded")

    page.locator("#startStopButton").click()
    page.wait_for_timeout(3000)
    page.locator("#startStopButton").click()

    val = page.locator("[role='progressbar']").get_attribute("aria-valuenow")
    assert val and 0 < int(val) < 100, f"Progress should be intermediate, got: {val}"
