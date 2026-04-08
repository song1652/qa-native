import re
import pytest
from playwright.sync_api import Page, expect

BASE_URL = "https://saintcore.kr"


def test_login_success(page: Page):
    page.goto(f"{BASE_URL}/member/login.html")
    page.wait_for_load_state("networkidle")

    page.fill("#member_id", "skj942")
    page.fill("#member_passwd", "danawa1631")
    page.click("a.btnSubmit")

    page.wait_for_load_state("networkidle")

    # After login, should be redirected away from login page
    expect(page).not_to_have_url(re.compile(r"/member/login\.html"))
