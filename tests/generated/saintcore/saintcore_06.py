import re
import pytest
from playwright.sync_api import Page, expect

BASE_URL = "https://saintcore.kr"


def test_access_mypage_after_login(page: Page):
    # Login
    page.goto(f"{BASE_URL}/member/login.html")
    page.wait_for_load_state("networkidle")

    page.fill("#member_id", "skj942")
    page.fill("#member_passwd", "danawa1631")
    page.click("a.btnSubmit")
    page.wait_for_load_state("networkidle")

    # Confirm logged in
    expect(page).not_to_have_url(re.compile(r"/member/login\.html"))

    # Navigate to mypage
    page.goto(f"{BASE_URL}/mypage/index.html")
    page.wait_for_load_state("networkidle")

    # Should be on mypage (not redirected to login)
    expect(page).not_to_have_url(re.compile(r"/member/login\.html"))
    expect(page).to_have_url(re.compile(r"/mypage/"))
