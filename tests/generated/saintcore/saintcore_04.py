import pytest
from playwright.sync_api import Page, expect

BASE_URL = "https://saintcore.kr"


def test_login_fails_with_empty_password(page: Page):
    page.goto(f"{BASE_URL}/member/login.html")
    page.wait_for_load_state("networkidle")

    # Fill ID only, leave password empty
    page.fill("#member_id", "skj942")
    page.click("a.btnSubmit")

    page.wait_for_load_state("networkidle")

    # Should stay on login page (not logged in)
    current_url = page.url
    assert "/member/login" in current_url or page.locator(
        ".alert, .error, #alert_msg"
    ).count() > 0
