import json
from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_slider_drag_updates_value_in_text_field(page: Page):
    page.goto(f"{BASE_URL}/slider", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)
    page.evaluate(
        "document.querySelectorAll('ins.adsbygoogle, iframe[src*=google], iframe[src*=doubleclick], #fixedban, footer').forEach(e => e.remove())"
    )

    # Get initial slider value
    value_input = page.locator("#sliderValue")
    expect(value_input).to_be_visible(timeout=10000)
    initial_value = value_input.input_value()

    # Drag slider to the right using JS mouse events
    slider = page.locator("input[type='range'].range-slider")
    expect(slider).to_be_visible(timeout=10000)

    box = slider.bounding_box()
    assert box is not None, "Slider bounding box not found"

    start_x = box["x"] + box["width"] * 0.25
    end_x = box["x"] + box["width"] * 0.75
    mid_y = box["y"] + box["height"] / 2

    page.mouse.move(start_x, mid_y)
    page.mouse.down()
    page.wait_for_timeout(100)
    page.mouse.move(end_x, mid_y, steps=10)
    page.wait_for_timeout(100)
    page.mouse.up()
    page.wait_for_timeout(500)

    new_value = value_input.input_value()
    assert new_value != initial_value, (
        f"Expected slider value to change from {initial_value}, but got {new_value}"
    )
    assert int(new_value) > int(initial_value), (
        f"Expected slider value to increase, got {initial_value} -> {new_value}"
    )
