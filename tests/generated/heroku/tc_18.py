import pytest
import json
import re
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_dynamic_loading_element_wait(page):
    page.goto(BASE_URL + "dynamic_loading/1")
    page.locator("#start button").click()
    expect(page.locator("#finish h4")).to_contain_text("Hello World!", timeout=15000)
