from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"


def test_form_date_picker_selection(page: Page):
    page.goto(f"{BASE_URL}/automation-practice-form", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    # Remove ads/overlays
    page.evaluate(
        "document.querySelectorAll('ins.adsbygoogle, iframe[src*=google], "
        "iframe[src*=doubleclick], #fixedban, footer').forEach(e => e.remove())"
    )

    # Open the Date of Birth date picker
    dob_input = page.locator("#dateOfBirthInput")
    dob_input.click()
    page.wait_for_timeout(500)

    # Select year 1990 from the year dropdown
    year_select = page.locator(".react-datepicker__year-select")
    year_select.select_option("1990")
    page.wait_for_timeout(300)

    # Select January from the month dropdown
    month_select = page.locator(".react-datepicker__month-select")
    month_select.select_option("0")  # January is index 0
    page.wait_for_timeout(300)

    # Click day 15
    page.locator(".react-datepicker__day--015:not(.react-datepicker__day--outside-month)").click()

    # Date picker should close and value should reflect selected date
    expect(page.locator(".react-datepicker")).to_be_hidden(timeout=3000)
    expect(dob_input).to_have_value("15 Jan 1990", timeout=5000)
