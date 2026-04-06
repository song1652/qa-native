from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_checkbox_2_toggle(page: Page):
    page.goto(BASE_URL + "checkboxes")
    page.wait_for_load_state("domcontentloaded")

    checkboxes = page.locator("form#checkboxes input[type='checkbox']")
    second_checkbox = checkboxes.nth(1)

    expect(second_checkbox).to_be_checked(timeout=5000)

    second_checkbox.click()

    expect(second_checkbox).not_to_be_checked(timeout=5000)
