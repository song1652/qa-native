import pytest
import json
import re
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_key_press_detection(page):
    page.goto(BASE_URL + "key_presses")
    page.locator("#target").click()
    page.keyboard.press("A")
    expect(page.locator("#result")).to_contain_text("You entered: A", timeout=10000)
