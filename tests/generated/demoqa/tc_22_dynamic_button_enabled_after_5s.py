from playwright.sync_api import expect
from pathlib import Path

BASE_URL = "https://demoqa.com"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"
_RM_ADS = "document.querySelectorAll('ins.adsbygoogle,iframe[src*=google],iframe[src*=doubleclick],#adplus-anchor,.ad-container').forEach(e=>e.remove())"  # noqa: E501


def test_dynamic_button_enabled_after_5s(page):
    page.goto(f"{BASE_URL}/dynamic-properties", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)
    page.evaluate(_RM_ADS)

    enable_btn = page.locator("#enableAfter")
    # Verify initially disabled
    expect(enable_btn).to_be_disabled(timeout=5000)

    # Wait for the button to become enabled (5 seconds + buffer)
    expect(enable_btn).to_be_enabled(timeout=10000)
