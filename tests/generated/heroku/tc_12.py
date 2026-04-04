import pytest
import json
import re
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_dynamic_controls_checkbox(page):
    page.goto(BASE_URL + "dynamic_controls")

    # Click Remove button inside #checkbox-example
    page.locator("#checkbox-example button").filter(has_text="Remove").click()

    # Wait for message to appear (avoid #loading strict mode - 2 elements on page)
    expect(page.locator("#message")).to_contain_text("It's gone!", timeout=10000)

    # Verify checkbox is gone
    expect(page.locator("#checkbox-example #checkbox")).to_have_count(0, timeout=10000)

    # Verify message "It's gone!"
    expect(page.locator("#message")).to_contain_text("It's gone!", timeout=10000)

    # Click Add button inside #checkbox-example
    page.locator("#checkbox-example button").filter(has_text="Add").click()

    # Wait for message to appear
    expect(page.locator("#message")).to_contain_text("It's back!", timeout=10000)

    # Verify checkbox is back
    expect(page.locator("#checkbox-example #checkbox")).to_have_count(1, timeout=10000)

    # Verify message "It's back!"
    expect(page.locator("#message")).to_contain_text("It's back!", timeout=10000)
