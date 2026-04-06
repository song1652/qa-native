"""Playwright 테스트 — test_header_logo (tc_97)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_header_logo(page):
    """Header logo is visible"""
    page.goto(BASE_URL)
    page.wait_for_load_state("domcontentloaded")

    logo = page.locator("header img, a[href='/'] img").first
    expect(logo).to_be_visible(timeout=5000)
