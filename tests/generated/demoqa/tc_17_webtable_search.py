"""Playwright 테스트 — test_webtable_search (tc_17)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_webtable_search(page):
    """Search records in web table"""
    page.goto(BASE_URL + "/webtables")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(1000)

    page.locator("#searchBox").fill("Cierra")
    page.wait_for_timeout(500)

    expect(page.locator("table tbody")).to_contain_text("Cierra", timeout=5000)
    # Non-matching record should not be visible
    body_text = page.locator("table tbody").inner_text()
    assert "Alden" not in body_text, "Alden should be filtered out"
