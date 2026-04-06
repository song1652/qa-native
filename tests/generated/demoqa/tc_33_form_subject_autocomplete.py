"""Playwright 테스트 — test_form_subject_autocomplete (tc_33)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_form_subject_autocomplete(page):
    """Form subject autocomplete"""
    page.goto(BASE_URL + "/automation-practice-form")
    page.wait_for_load_state("domcontentloaded")

    page.locator("#subjectsInput").fill("Ma")
    page.wait_for_timeout(500)
    page.locator(".subjects-auto-complete__option:has-text('Maths')").click()

    expect(page.locator(".subjects-auto-complete__multi-value__label")).to_contain_text("Maths", timeout=5000)
