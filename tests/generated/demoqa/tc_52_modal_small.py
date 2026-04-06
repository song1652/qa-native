"""Playwright 테스트 — test_modal_small (tc_52)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_modal_small(page):
    """Small modal opens and can be closed"""
    page.goto(BASE_URL + "/modal-dialogs")
    page.wait_for_load_state("domcontentloaded")

    page.locator("#showSmallModal").click()
    expect(page.locator(".modal-body")).to_be_visible(timeout=5000)
    expect(page.locator(".modal-body")).to_contain_text("small modal")

    page.locator("#closeSmallModal").click()
    expect(page.locator(".modal-dialog")).not_to_be_visible(timeout=10000)
