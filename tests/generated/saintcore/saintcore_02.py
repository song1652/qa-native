import pytest
from playwright.sync_api import Page, expect

BASE_URL = "https://saintcore.kr"


def test_wrong_password_shows_error_message(page: Page):
    page.goto(f"{BASE_URL}/member/login.html")
    page.wait_for_load_state("networkidle")

    page.fill("#member_id", "skj942")
    page.fill("#member_passwd", "wrongpass123")
    page.click("a.btnSubmit")

    page.wait_for_load_state("networkidle")

    # Should stay on login page or show error message
    current_url = page.url
    assert "/member/login" in current_url or page.locator(
        ".alert, .error, #alert_msg, .login_error"
    ).count() > 0
