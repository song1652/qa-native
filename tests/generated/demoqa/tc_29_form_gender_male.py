"""Playwright 테스트 — test_form_gender_male (tc_29)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_form_gender_male(page):
    """Form gender Male selection"""
    page.goto(BASE_URL + "/automation-practice-form")
    page.wait_for_load_state("domcontentloaded")

    page.locator("label[for='gender-radio-1']").click()
    expect(page.locator("#gender-radio-1")).to_be_checked(timeout=5000)
