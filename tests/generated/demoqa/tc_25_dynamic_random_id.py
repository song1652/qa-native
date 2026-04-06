"""Playwright 테스트 — test_dynamic_random_id (tc_25)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_dynamic_random_id(page):
    """Button ID changes on each page load"""
    page.goto(BASE_URL + "/dynamic-properties")
    page.wait_for_load_state("domcontentloaded")

    random_text = page.locator("p:has-text('This text has random Id')")
    first_id = random_text.get_attribute("id")
    assert first_id, "Element should have an id"

    page.reload()
    page.wait_for_load_state("domcontentloaded")

    random_text2 = page.locator("p:has-text('This text has random Id')")
    second_id = random_text2.get_attribute("id")
    assert second_id != first_id, f"ID should change: {first_id} vs {second_id}"
