from playwright.sync_api import expect
from pathlib import Path

BASE_URL = "https://demoqa.com"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"

AD_REMOVE_JS = (
    "document.querySelectorAll("
    "'ins.adsbygoogle, iframe[src*=google], iframe[src*=doubleclick]'"
    ").forEach(e => e.remove())"
)


def test_links_no_content_api(page):
    page.goto(f"{BASE_URL}/links", wait_until="domcontentloaded")
    page.evaluate(AD_REMOVE_JS)
    page.wait_for_timeout(2000)

    # Click "No Content" API call link
    no_content_link = page.locator("#no-content")
    expect(no_content_link).to_be_visible(timeout=10000)
    no_content_link.click()

    # Wait for response message to appear
    link_response = page.locator("#linkResponse")
    expect(link_response).to_be_visible(timeout=10000)
    expect(link_response).to_contain_text("204", timeout=10000)
    expect(link_response).to_contain_text("No Content", timeout=10000)
