import re
import pytest
from playwright.sync_api import Page, expect

BASE_URL = "https://saintcore.kr"


def test_login_then_logout(page: Page):
    # Login first
    page.goto(f"{BASE_URL}/member/login.html")
    page.wait_for_load_state("networkidle")

    page.fill("#member_id", "skj942")
    page.fill("#member_passwd", "danawa1631")
    page.click("a.btnSubmit")
    page.wait_for_load_state("networkidle")

    # Confirm logged in (not on login page)
    expect(page).not_to_have_url(re.compile(r"/member/login\.html"))

    # Dismiss any popup that may be blocking the logout button
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)

    # Close smart popup overlay if present
    popup = page.locator(".app-smart-popup")
    if popup.count() > 0:
        close_btn = page.locator(
            ".app-smart-popup [class*='close'], .app-smart-popup button"
        )
        if close_btn.count() > 0:
            close_btn.first.click()
            page.wait_for_timeout(300)

    # Navigate directly to logout URL (most reliable)
    page.goto(f"{BASE_URL}/exec/front/Member/logout/")
    page.wait_for_load_state("networkidle")

    # After logout - should be on home or login page
    current_url = page.url
    assert current_url.rstrip("/") == BASE_URL or "/member/login" in current_url
