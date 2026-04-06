from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_horizontal_slider_min(page: Page):
    """TC-118: 수평 슬라이더 최소값 설정 - 슬라이더를 0으로 이동"""
    page.goto("https://the-internet.herokuapp.com/horizontal_slider")
    page.wait_for_load_state("domcontentloaded")

    slider = page.locator("input[type='range']")
    expect(slider).to_be_visible(timeout=10000)

    # Home 키로 최소값으로 이동
    slider.focus()
    page.keyboard.press("Home")

    value_display = page.locator("#range")
    expect(value_display).to_have_text("0", timeout=5000)
