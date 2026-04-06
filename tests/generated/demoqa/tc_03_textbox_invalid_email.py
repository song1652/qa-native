"""Playwright 테스트 — test_textbox_invalid_email (tc_03)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_textbox_invalid_email(page):
    """Submit text box with invalid email"""
    page.goto(BASE_URL + "/text-box")
    page.wait_for_load_state("domcontentloaded")

    page.locator("#userEmail").fill("invalid-email")
    page.locator("#submit").scroll_into_view_if_needed()
    page.locator("#submit").click()
    page.wait_for_timeout(500)

    # Email field should have error class
    email_field = page.locator("#userEmail")
    cls = email_field.get_attribute("class") or ""
    assert "field-error" in cls, f"Email field should have error class, got: {cls}"
