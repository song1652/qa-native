from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_dropdown_select_option2(page: Page):
    page.goto(BASE_URL + "dropdown")
    page.wait_for_load_state("domcontentloaded")

    dropdown = page.locator("#dropdown")
    dropdown.select_option(value="2")

    expect(dropdown).to_have_value("2", timeout=5000)
    selected = page.locator("#dropdown option:checked")
    expect(selected).to_contain_text("Option 2", timeout=5000)
