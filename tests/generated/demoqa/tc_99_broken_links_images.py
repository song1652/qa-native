"""Playwright 테스트 — test_broken_links_images (tc_99)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_broken_links_images(page):
    """Valid link on broken links page"""
    page.goto(BASE_URL + "/broken")
    page.wait_for_load_state("domcontentloaded")

    valid_link = page.locator("a:has-text('Click Here for Valid Link')")
    expect(valid_link).to_be_visible(timeout=5000)
    valid_link.click()
    page.wait_for_load_state("domcontentloaded")

    assert page.url != BASE_URL + "/broken"
