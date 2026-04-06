"""Playwright 테스트 — test_homepage_load (tc_91)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_homepage_load(page):
    """Homepage load"""
    page.goto(BASE_URL)
    page.wait_for_load_state("domcontentloaded")

    cards = page.locator(".card-body h5")
    expect(cards).to_have_count(6, timeout=10000)
