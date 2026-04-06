import json
from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_slider_default_value_is_25(page: Page):
    page.goto(f"{BASE_URL}/slider", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)
    page.evaluate(
        "document.querySelectorAll('ins.adsbygoogle, iframe[src*=google], iframe[src*=doubleclick], #fixedban, footer').forEach(e => e.remove())"
    )

    # Verify slider default value
    slider = page.locator("input[type='range'].range-slider")
    expect(slider).to_be_visible(timeout=10000)
    slider_value = slider.get_attribute("value")
    assert slider_value == "25", f"Expected slider default value to be 25, got {slider_value}"

    # Verify the text field shows the same default value
    value_input = page.locator("#sliderValue")
    expect(value_input).to_be_visible(timeout=10000)
    text_value = value_input.input_value()
    assert text_value == "25", f"Expected text field to show 25, got {text_value}"

    assert slider_value == text_value, (
        f"Slider position ({slider_value}) and text field ({text_value}) do not match"
    )
