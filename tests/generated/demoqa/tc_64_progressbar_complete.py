"""Playwright 테스트 — test_progressbar_complete (tc_64)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_progressbar_complete(page):
    """Progress bar completes to 100%"""
    page.goto(BASE_URL + "/progress-bar")
    page.wait_for_load_state("domcontentloaded")

    page.locator("#startStopButton").click()

    expect(page.locator("[role='progressbar']")).to_have_attribute(
        "aria-valuenow", "100", timeout=25000
    )
    expect(page.locator("#resetButton")).to_be_visible(timeout=5000)
