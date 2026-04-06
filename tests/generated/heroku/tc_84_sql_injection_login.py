from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_sql_injection_login(page: Page):
    page.goto(BASE_URL + "login")
    page.wait_for_load_state("domcontentloaded")

    page.locator("#username").fill("' OR '1'='1")
    page.locator("#password").fill("' OR '1'='1")
    page.locator("button[type='submit']").click()

    expect(page.locator("#flash")).to_contain_text(
        "Your username is invalid!", timeout=10000
    )
