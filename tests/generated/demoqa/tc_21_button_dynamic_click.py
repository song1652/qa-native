from playwright.sync_api import expect
from pathlib import Path

BASE_URL = "https://demoqa.com"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"
_RM_ADS = "document.querySelectorAll('ins.adsbygoogle,iframe[src*=google],iframe[src*=doubleclick],#adplus-anchor,.ad-container').forEach(e=>e.remove())"  # noqa: E501


def test_button_dynamic_click(page):
    page.goto(f"{BASE_URL}/buttons", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)
    page.evaluate(_RM_ADS)

    # The dynamic click button is the last "Click Me" button (after right-click and double-click)
    dynamic_click_btn = page.locator("button:has-text('Click Me')").last
    dynamic_click_btn.click()

    expect(page.locator("#dynamicClickMessage")).to_be_visible(timeout=10000)
    expect(page.locator("#dynamicClickMessage")).to_contain_text("You have done a dynamic click")
