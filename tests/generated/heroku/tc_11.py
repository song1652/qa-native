import pytest
import json
import re
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_hover_user_info(page):
    page.goto(BASE_URL + "hovers")
    first_figure = page.locator(".figure").first
    first_figure.hover()
    # The hovers page uses div.figcaption > h5 and a, not <figcaption> element
    expect(first_figure.locator(".figcaption h5")).to_contain_text("name: user1", timeout=5000)
    expect(first_figure.locator(".figcaption a")).to_be_visible(timeout=5000)
    expect(first_figure.locator(".figcaption a")).to_contain_text("View profile", timeout=5000)
