import pytest
import json
import re
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_dynamic_controls_input_enable(page):
    page.goto(BASE_URL + "dynamic_controls")

    input_field = page.locator("#input-example input[type='text']")
    expect(input_field).to_be_disabled()

    page.locator("#input-example button").click()

    expect(input_field).to_be_enabled(timeout=10000)
    expect(page.locator("#message")).to_contain_text("It's enabled!")
