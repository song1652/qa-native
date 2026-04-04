import pytest
import json
import re
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_horizontal_slider(page):
    page.goto(BASE_URL + "horizontal_slider")

    slider = page.locator("input[type='range']")
    slider.click()

    for _ in range(5):
        page.keyboard.press("ArrowRight")

    span = page.locator("span#range")
    expect(span).not_to_have_text("0", timeout=5000)
