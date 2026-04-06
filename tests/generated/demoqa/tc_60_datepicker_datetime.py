"""Playwright 테스트 — test_datepicker_datetime (tc_60)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_datepicker_datetime(page):
    """Date and time picker"""
    page.goto(BASE_URL + "/date-picker")
    page.wait_for_load_state("domcontentloaded")

    page.locator("#dateAndTimePickerInput").click()
    page.locator(".react-datepicker__day--015:not(.react-datepicker__day--outside-month)").click()

    val = page.locator("#dateAndTimePickerInput").input_value()
    assert val, "DateTime should be selected"
