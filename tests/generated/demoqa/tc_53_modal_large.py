"""Playwright 테스트 — test_modal_large (tc_53)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_modal_large(page):
    """Large modal opens and can be closed"""
    page.goto(BASE_URL + "/modal-dialogs")
    page.wait_for_load_state("domcontentloaded")

    page.locator("#showLargeModal").click()
    expect(page.locator(".modal-body")).to_be_visible(timeout=5000)

    page.locator("#closeLargeModal").click()
    expect(page.locator(".modal-dialog")).not_to_be_visible(timeout=10000)
