import re
from playwright.sync_api import expect
from pathlib import Path

BASE_URL = "https://demoqa.com"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"

AD_REMOVE_JS = (
    "document.querySelectorAll("
    "'ins.adsbygoogle, iframe[src*=google], iframe[src*=doubleclick]'"
    ").forEach(e => e.remove())"
)


def test_links_home_link(page):
    page.goto(f"{BASE_URL}/links", wait_until="domcontentloaded")
    page.evaluate(AD_REMOVE_JS)
    page.wait_for_timeout(2000)

    # Find the "Home" link that opens a new tab
    home_link = page.locator("#simpleLink")
    expect(home_link).to_be_visible(timeout=10000)

    # Wait for the new page/tab to open
    with page.context.expect_page(timeout=15000) as new_page_info:
        home_link.click()

    new_page = new_page_info.value
    new_page.wait_for_load_state("domcontentloaded", timeout=15000)

    # Verify the new tab URL is demoqa.com home
    expect(new_page).to_have_url(re.compile(r"https://demoqa\.com/?$"), timeout=10000)
