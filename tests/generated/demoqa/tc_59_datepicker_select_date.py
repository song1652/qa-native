from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"


def test_date_picker_selects_and_displays_date(page: Page):
    page.goto(f"{BASE_URL}/date-picker")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(2000)

    # Remove ads/overlays
    page.evaluate(
        "document.querySelectorAll('ins.adsbygoogle, iframe[src*=google], "
        "iframe[src*=doubleclick], #fixedban, footer').forEach(e => e.remove())"
    )

    # Get the Select Date input field
    date_input = page.locator("#datePickerMonthYearInput")
    expect(date_input).to_be_visible(timeout=10000)

    # Click the date input to open calendar
    date_input.click()
    page.wait_for_timeout(500)

    # Calendar should open - select a day (e.g., 15)
    # Find a day cell that is not from previous/next month
    day_cell = page.locator(
        ".react-datepicker__day:not(.react-datepicker__day--outside-month)"
    ).filter(has_text="15").first
    expect(day_cell).to_be_visible(timeout=5000)
    day_cell.click()
    page.wait_for_timeout(300)

    # Verify the date input has a value (date was selected)
    date_value = date_input.input_value()
    assert date_value != "", "Date field should have a value after selection, got empty string"
    assert "15" in date_value, f"Selected date '15' should appear in field value, got: {date_value!r}"
