from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_checkbox_initial_state(page: Page):
    page.goto(BASE_URL + "checkboxes")
    page.wait_for_load_state("domcontentloaded")

    checkboxes = page.locator("form#checkboxes input[type='checkbox']")
    expect(checkboxes).to_have_count(2, timeout=5000)

    expect(checkboxes.nth(0)).not_to_be_checked(timeout=5000)
    expect(checkboxes.nth(1)).to_be_checked(timeout=5000)
