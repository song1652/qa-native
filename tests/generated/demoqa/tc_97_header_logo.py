from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"


def test_header_logo(page: Page):
    page.goto(BASE_URL + "/", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    logo = page.locator("header img").first
    expect(logo).to_be_visible(timeout=10000)
