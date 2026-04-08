from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"
TEST_DATA_PATH = (
    Path(__file__).resolve().parent.parent.parent.parent
    / "config" / "test_data.json"
)


def test_dynamic_button_initial_disabled(page: Page):
    page.goto(f"{BASE_URL}/dynamic-properties")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(2000)

    # Remove ads/overlays
    page.evaluate(
        "document.querySelectorAll("
        "'ins.adsbygoogle, iframe[src*=google],"
        " iframe[src*=doubleclick], #fixedban, footer'"
        ").forEach(e => e.remove())"
    )

    # Button should be disabled immediately after page load
    will_enable_btn = page.locator("button").filter(
        has_text="Will enable 5 seconds"
    )
    expect(will_enable_btn).to_be_visible(timeout=5000)
    expect(will_enable_btn).to_be_disabled(timeout=3000)
