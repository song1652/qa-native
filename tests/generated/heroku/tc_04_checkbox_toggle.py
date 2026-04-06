from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_checkbox_toggle(page: Page) -> None:
    page.goto("https://the-internet.herokuapp.com/checkboxes")
    page.wait_for_load_state("domcontentloaded")

    checkboxes = page.locator("form#checkboxes input[type='checkbox']")
    expect(checkboxes).to_have_count(2)

    checkbox1 = checkboxes.nth(0)
    checkbox2 = checkboxes.nth(1)

    # checkbox1 is initially unchecked — click to check it
    if not checkbox1.is_checked():
        checkbox1.click()

    # checkbox2 is initially checked — click to uncheck it
    if checkbox2.is_checked():
        checkbox2.click()

    expect(checkbox1).to_be_checked()
    expect(checkbox2).not_to_be_checked()
