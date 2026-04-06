from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_horizontal_slider_max(page: Page):
    """TC-119: 수평 슬라이더 최대값 설정 - 슬라이더를 5로 이동"""
    page.goto("https://the-internet.herokuapp.com/horizontal_slider")
    page.wait_for_load_state("domcontentloaded")

    slider = page.locator("input[type='range']")
    expect(slider).to_be_visible(timeout=10000)

    # End 키로 최대값으로 이동
    slider.focus()
    page.keyboard.press("End")

    value_display = page.locator("#range")
    expect(value_display).to_have_text("5", timeout=5000)
