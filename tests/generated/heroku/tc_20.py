import pytest
import json
import re
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_number_input_field(page):
    page.goto(BASE_URL + "inputs")

    input_field = page.locator("input[type='number']")

    input_field.fill("42")

    expect(input_field).to_have_value("42", timeout=5000)
    expect(input_field).to_have_attribute("type", "number", timeout=5000)
