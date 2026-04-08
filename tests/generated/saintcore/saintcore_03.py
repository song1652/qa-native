import pytest
from playwright.sync_api import Page, expect

BASE_URL = "https://saintcore.kr"


def test_login_fails_with_empty_id(page: Page):
    page.goto(f"{BASE_URL}/member/login.html")
    page.wait_for_load_state("networkidle")

    # Leave ID empty, fill password only
    page.fill("#member_passwd", "danawa1631")
    page.click("a.btnSubmit")

    page.wait_for_load_state("networkidle")

    # Should stay on login page (not logged in)
    current_url = page.url
    assert "/member/login" in current_url or page.locator(
        ".alert, .error, #alert_msg"
    ).count() > 0
