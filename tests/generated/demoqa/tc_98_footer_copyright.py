"""Playwright 테스트 — test_footer_copyright (tc_98)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_footer_copyright(page):
    """Footer copyright text"""
    page.goto(BASE_URL)
    page.wait_for_load_state("domcontentloaded")

    footer = page.locator("footer, #linkWrapper")
    expect(footer).to_be_visible(timeout=5000)
