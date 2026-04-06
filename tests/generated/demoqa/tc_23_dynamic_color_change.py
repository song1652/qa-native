"""Playwright 테스트 — test_dynamic_color_change (tc_23)"""
import re
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_dynamic_color_change(page):
    """Button color changes after 5 seconds"""
    page.goto(BASE_URL + "/dynamic-properties")
    page.wait_for_load_state("domcontentloaded")

    btn = page.locator("#colorChange")
    expect(btn).to_have_class(re.compile("text-danger"), timeout=10000)
