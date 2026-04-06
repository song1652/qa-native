"""Playwright 테스트 — test_form_dob_year_change (tc_115)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_form_dob_year_change(page):
    """Form DOB year change"""
    page.goto(BASE_URL + "/automation-practice-form")
    page.wait_for_load_state("domcontentloaded")

    page.locator("#dateOfBirthInput").click()
    page.locator(".react-datepicker__year-select").select_option("1990")

    year_val = page.locator(".react-datepicker__year-select").input_value()
    assert year_val == "1990", f"Year should be 1990, got: {year_val}"
