"""Playwright 테스트 — test_autocomplete_single (tc_58)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_autocomplete_single(page):
    """Auto complete single color selection"""
    page.goto(BASE_URL + "/auto-complete")
    page.wait_for_load_state("domcontentloaded")

    page.locator("#autoCompleteSingleInput").fill("Gr")
    page.wait_for_timeout(500)
    page.locator(".auto-complete__option:has-text('Green')").click()

    expect(page.locator(".auto-complete__single-value")).to_have_text("Green", timeout=5000)
