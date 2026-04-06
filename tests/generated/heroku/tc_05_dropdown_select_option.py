from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_dropdown_select_option(page: Page) -> None:
    page.goto("https://the-internet.herokuapp.com/dropdown")
    page.wait_for_load_state("domcontentloaded")

    dropdown = page.locator("#dropdown")

    dropdown.select_option("1")
    expect(dropdown).to_have_value("1")

    dropdown.select_option("2")
    expect(dropdown).to_have_value("2")
