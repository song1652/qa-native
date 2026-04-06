import re
from playwright.sync_api import expect
from pathlib import Path

BASE_URL = "https://demoqa.com"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"
_RM_ADS = "document.querySelectorAll('ins.adsbygoogle,iframe[src*=google],iframe[src*=doubleclick],#adplus-anchor,.ad-container').forEach(e=>e.remove())"  # noqa: E501


def test_dynamic_color_change(page):
    page.goto(f"{BASE_URL}/dynamic-properties", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)
    page.evaluate(_RM_ADS)

    color_change_btn = page.locator("#colorChange")

    # Wait for the text-danger class to be added (~5 seconds after page load)
    expect(color_change_btn).to_have_class(re.compile(r"text-danger"), timeout=10000)
