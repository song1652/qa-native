from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_slider_value_manipulation(page: Page):
    """슬라이더 값 조작"""
    page.goto("https://the-internet.herokuapp.com/horizontal_slider")
    page.wait_for_load_state("domcontentloaded")

    slider = page.locator("input[type='range']")
    expect(slider).to_be_visible(timeout=10000)

    slider.click()
    for _ in range(5):
        slider.press("ArrowRight")

    value_display = page.locator("#range")
    expect(value_display).to_be_visible(timeout=5000)
    value_text = value_display.inner_text()
    assert float(value_text) > 0, f"Slider value should be > 0, got: {value_text}"
