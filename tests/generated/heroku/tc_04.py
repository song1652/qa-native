import pytest
import json
import re
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_checkbox_toggle(page):
    page.goto(BASE_URL + "checkboxes")

    first_checkbox = page.locator("input[type='checkbox']").nth(0)
    second_checkbox = page.locator("input[type='checkbox']").nth(1)

    first_checkbox.click()
    second_checkbox.click()

    expect(first_checkbox).to_be_checked(timeout=5000)
    expect(second_checkbox).not_to_be_checked(timeout=5000)
