import pytest
import json
import re
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_dropdown_option_select(page):
    page.goto(BASE_URL + "dropdown")

    dropdown = page.locator("#dropdown")

    page.select_option("#dropdown", "1")
    expect(dropdown).to_have_value("1", timeout=5000)

    page.select_option("#dropdown", "2")
    expect(dropdown).to_have_value("2", timeout=5000)
