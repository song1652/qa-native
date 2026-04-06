"""Playwright 테스트 — test_slider_input_value (tc_62)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_slider_input_value(page):
    """Slider default value is 25"""
    page.goto(BASE_URL + "/slider")
    page.wait_for_load_state("domcontentloaded")

    val = page.locator("#sliderValue").get_attribute("value")
    assert val == "25", f"Default slider value should be 25, got: {val}"
