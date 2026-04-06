"""Playwright 테스트 — test_slider_drag (tc_61)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_slider_drag(page):
    """Slider drag updates value"""
    page.goto(BASE_URL + "/slider")
    page.wait_for_load_state("domcontentloaded")

    slider = page.locator("input[type='range']")
    box = slider.bounding_box()
    # Drag to right
    page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
    page.mouse.down()
    page.mouse.move(box["x"] + box["width"] * 0.8, box["y"] + box["height"] / 2, steps=10)
    page.mouse.up()
    page.wait_for_timeout(300)

    val = page.locator("#sliderValue").get_attribute("value")
    assert val and int(val) > 25, f"Slider should move right, got: {val}"
