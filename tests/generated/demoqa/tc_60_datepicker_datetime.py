import json
from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_datepicker_datetime_selects_and_displays(page: Page):
    # Remove ads/overlays
    page.goto(f"{BASE_URL}/date-picker", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)
    page.evaluate(
        "document.querySelectorAll('ins.adsbygoogle, iframe[src*=google], iframe[src*=doubleclick], #fixedban, footer').forEach(e => e.remove())"
    )

    # Click the Date And Time picker field
    date_time_input = page.locator("#dateAndTimePickerInput")
    expect(date_time_input).to_be_visible(timeout=10000)
    date_time_input.click()
    page.wait_for_timeout(500)

    # Select a month from the month dropdown
    month_select = page.locator(".react-datepicker__month-select")
    if month_select.is_visible():
        month_select.select_option("January")
        page.wait_for_timeout(300)

    # Select a year from the year dropdown
    year_select = page.locator(".react-datepicker__year-select")
    if year_select.is_visible():
        year_select.select_option("2025")
        page.wait_for_timeout(300)

    # Click a day
    day = page.locator(".react-datepicker__day:not(.react-datepicker__day--outside-month)").first
    expect(day).to_be_visible(timeout=5000)
    day.click()
    page.wait_for_timeout(500)

    # Select time if time list is visible
    time_item = page.locator(".react-datepicker__time-list-item").first
    if time_item.is_visible():
        time_item.click()
        page.wait_for_timeout(300)

    # Verify the input has a non-empty value
    value = date_time_input.input_value()
    assert value != "", f"Expected date-time input to have a value, got empty string"
