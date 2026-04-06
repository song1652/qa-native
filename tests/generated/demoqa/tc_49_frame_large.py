"""Playwright 테스트 — test_frame_large (tc_49)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_frame_large(page):
    """Large iframe contains sample page text"""
    page.goto(BASE_URL + "/frames")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(1000)

    frame = page.frame_locator("#frame1")
    expect(frame.locator("#sampleHeading")).to_have_text(
        "This is a sample page", timeout=15000
    )
