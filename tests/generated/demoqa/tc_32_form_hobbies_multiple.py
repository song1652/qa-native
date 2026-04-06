"""Playwright 테스트 — test_form_hobbies_multiple (tc_32)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_form_hobbies_multiple(page):
    """Form hobbies multiple selection"""
    page.goto(BASE_URL + "/automation-practice-form")
    page.wait_for_load_state("domcontentloaded")

    page.locator("label[for='hobbies-checkbox-1']").click()
    page.locator("label[for='hobbies-checkbox-2']").click()
    page.locator("label[for='hobbies-checkbox-3']").click()

    expect(page.locator("#hobbies-checkbox-1")).to_be_checked(timeout=5000)
    expect(page.locator("#hobbies-checkbox-2")).to_be_checked(timeout=5000)
    expect(page.locator("#hobbies-checkbox-3")).to_be_checked(timeout=5000)
