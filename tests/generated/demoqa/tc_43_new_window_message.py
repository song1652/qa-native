from playwright.sync_api import Page

BASE_URL = "https://demoqa.com"

AD_REMOVE_JS = (
    "document.querySelectorAll("
    "'ins.adsbygoogle, iframe[src*=google], iframe[src*=doubleclick], #fixedban, footer'"
    ").forEach(e => e.remove())"
)


def test_new_window_message_shows_message_text(page: Page):
    page.goto(f"{BASE_URL}/browser-windows")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(2000)

    page.evaluate(AD_REMOVE_JS)

    # Click New Window Message button and capture the new page/window
    with page.context.expect_page() as new_page_info:
        page.locator("#messageWindowButton").click()

    new_page = new_page_info.value
    new_page.wait_for_load_state("domcontentloaded")
    new_page.wait_for_timeout(1000)

    # Verify the new window has some message text (body is not empty)
    body_text = new_page.locator("body").inner_text()
    assert len(body_text.strip()) > 0, "New window message should contain some text"
