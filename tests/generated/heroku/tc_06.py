import pytest
import json
import re
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_add_remove_elements(page):
    page.goto(BASE_URL + "add_remove_elements/")

    add_button = page.get_by_role("button", name="Add Element")
    add_button.click()
    add_button.click()
    add_button.click()

    expect(page.locator(".added-manually")).to_have_count(3, timeout=5000)

    page.locator(".added-manually").first.click()

    expect(page.locator(".added-manually")).to_have_count(2, timeout=5000)
