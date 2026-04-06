from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_checkbox_1_toggle(page: Page):
    page.goto(BASE_URL + "checkboxes")
    page.wait_for_load_state("domcontentloaded")

    checkboxes = page.locator("form#checkboxes input[type='checkbox']")
    first_checkbox = checkboxes.nth(0)

    expect(first_checkbox).not_to_be_checked(timeout=5000)

    first_checkbox.click()

    expect(first_checkbox).to_be_checked(timeout=5000)
