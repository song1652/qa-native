from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"


def test_footer_copyright(page: Page):
    page.goto(BASE_URL + "/", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    footer = page.locator("footer")
    expect(footer).to_be_visible(timeout=10000)
    expect(footer).to_contain_text("TOOLSQA.COM", timeout=5000)
