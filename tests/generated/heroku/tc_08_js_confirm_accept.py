from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_js_confirm_accept(page: Page) -> None:
    page.goto("https://the-internet.herokuapp.com/javascript_alerts")
    page.wait_for_load_state("domcontentloaded")

    page.on("dialog", lambda dialog: dialog.accept())

    page.get_by_role("button", name="Click for JS Confirm").click()

    expect(page.locator("#result")).to_contain_text("You clicked: Ok")
