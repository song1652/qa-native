from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"
TEST_DATA_PATH = (
    Path(__file__).resolve().parent.parent.parent.parent
    / "config" / "test_data.json"
)


def test_form_dob_year_change(page: Page):
    page.goto(f"{BASE_URL}/automation-practice-form")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(2000)

    # Remove ads/overlays
    page.evaluate(
        "document.querySelectorAll("
        "'ins.adsbygoogle, iframe[src*=google],"
        " iframe[src*=doubleclick], #fixedban, footer'"
        ").forEach(e => e.remove())"
    )

    # Click Date of Birth input to open calendar
    dob_input = page.locator("#dateOfBirthInput")
    dob_input.click()
    page.wait_for_timeout(500)

    # Select year from dropdown in calendar header
    year_select = page.locator(".react-datepicker__year-select")
    expect(year_select).to_be_visible(timeout=5000)
    year_select.select_option("1990")
    page.wait_for_timeout(500)

    # Verify year dropdown shows 1990
    expect(year_select).to_have_value("1990")
