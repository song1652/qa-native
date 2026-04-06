"""Playwright 테스트 — test_nested_frames (tc_51)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_nested_frames(page):
    """Nested frames show parent and child text"""
    page.goto(BASE_URL + "/nestedframes")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(1000)

    parent_frame = page.frame_locator("#frame1")
    expect(parent_frame.locator("body")).to_contain_text("Parent frame", timeout=10000)

    child_frame = parent_frame.frame_locator("iframe")
    expect(child_frame.locator("body")).to_contain_text("Child Iframe", timeout=10000)
