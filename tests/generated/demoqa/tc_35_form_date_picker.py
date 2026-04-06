"""Playwright 테스트 — test_form_date_picker (tc_35)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_form_date_picker(page):
    """Form date picker selection"""
    page.goto(BASE_URL + "/automation-practice-form")
    page.wait_for_load_state("domcontentloaded")

    page.locator("#dateOfBirthInput").click()
    page.locator(".react-datepicker__year-select").select_option("1990")
    page.locator(".react-datepicker__month-select").select_option("0")  # January
    page.locator(".react-datepicker__day--015:not(.react-datepicker__day--outside-month)").click()

    val = page.locator("#dateOfBirthInput").input_value()
    assert "1990" in val, f"Date should contain 1990, got: {val}"
