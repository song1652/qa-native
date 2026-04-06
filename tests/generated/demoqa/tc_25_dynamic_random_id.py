from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"
_RM_ADS = "document.querySelectorAll('ins.adsbygoogle,iframe[src*=google],iframe[src*=doubleclick],#adplus-anchor,.ad-container').forEach(e=>e.remove())"  # noqa: E501


def test_dynamic_random_id(page: Page):
    page.goto(f"{BASE_URL}/dynamic-properties", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)
    page.evaluate(_RM_ADS)

    # The page has a button that enables after 5 seconds (#enableAfter)
    # and a button that changes color (#colorChange)
    # Verify dynamic properties: enableAfter starts disabled and becomes enabled
    enable_btn = page.locator("#enableAfter")
    assert enable_btn.count() > 0, "enableAfter button not found"

    # Initially the button should be disabled
    is_disabled_initially = enable_btn.is_disabled()
    assert is_disabled_initially, "Expected button to be disabled initially"

    # Wait 5+ seconds for it to become enabled
    expect(enable_btn).to_be_enabled(timeout=10000)
    assert enable_btn.is_enabled(), "Expected button to be enabled after 5 seconds"
