"""Playwright 테스트 — test_datepicker_select_date (tc_59)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_datepicker_select_date(page):
    """Date picker selects and displays date"""
    page.goto(BASE_URL + "/date-picker")
    page.wait_for_load_state("domcontentloaded")

    page.locator("#datePickerMonthYearInput").click()
    # Select a day
    page.locator(".react-datepicker__day--015:not(.react-datepicker__day--outside-month)").click()

    val = page.locator("#datePickerMonthYearInput").input_value()
    assert val, "Date should be selected"
