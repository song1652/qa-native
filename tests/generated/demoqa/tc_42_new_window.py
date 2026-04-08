from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"

AD_REMOVE_JS = (
    "document.querySelectorAll("
    "'ins.adsbygoogle, iframe[src*=google], iframe[src*=doubleclick], #fixedban, footer'"
    ").forEach(e => e.remove())"
)


def test_new_window_opens_with_sample_page_text(page: Page):
    page.goto(f"{BASE_URL}/browser-windows")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(2000)

    page.evaluate(AD_REMOVE_JS)

    # Click New Window button and capture the new page/window
    with page.context.expect_page() as new_page_info:
        page.locator("#windowButton").click()

    new_page = new_page_info.value
    new_page.wait_for_load_state("domcontentloaded")
    new_page.wait_for_timeout(1000)

    # Verify the new window has the expected text
    expect(new_page.locator("body")).to_contain_text("This is a sample page", timeout=10000)
