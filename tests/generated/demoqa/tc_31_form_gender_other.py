"""Playwright 테스트 — test_form_gender_other (tc_31)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_form_gender_other(page):
    """Form gender Other selection"""
    page.goto(BASE_URL + "/automation-practice-form")
    page.wait_for_load_state("domcontentloaded")

    page.locator("label[for='gender-radio-3']").click()
    expect(page.locator("#gender-radio-3")).to_be_checked(timeout=5000)
