from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_add_remove_elements(page: Page) -> None:
    page.goto("https://the-internet.herokuapp.com/add_remove_elements/")
    page.wait_for_load_state("domcontentloaded")

    add_button = page.get_by_role("button", name="Add Element")

    add_button.click()
    add_button.click()
    add_button.click()

    delete_buttons = page.locator("#elements button.added-manually")
    expect(delete_buttons).to_have_count(3)

    delete_buttons.first.click()

    expect(delete_buttons).to_have_count(2)
