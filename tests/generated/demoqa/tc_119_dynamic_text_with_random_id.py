"""Playwright 테스트 — test_dynamic_text_with_random_id (tc_119)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_dynamic_text_with_random_id(page):
    """Dynamic text with random id"""
    page.goto(BASE_URL + "/dynamic-properties")
    page.wait_for_load_state("domcontentloaded")

    el = page.locator("p:has-text('This text has random Id')")
    expect(el).to_be_visible(timeout=5000)

    el_id = el.get_attribute("id")
    assert el_id and len(el_id) > 0, "Should have a non-empty id"
