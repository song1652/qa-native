import pytest
from playwright.sync_api import Page, expect

BASE_URL = "https://saintcore.kr"


def test_find_id_page_ui_visible(page: Page):
    page.goto(f"{BASE_URL}/member/login.html")
    page.wait_for_load_state("networkidle")

    # Click find ID link
    page.click(
        "a[href*='find_id'], a:has-text('아이디 찾기'), a:has-text('아이디찾기')"
    )
    page.wait_for_load_state("networkidle")

    # Should be on find ID page
    expect(page).to_have_url(f"{BASE_URL}/member/id/find_id.html")

    # Form or guide text should be visible
    assert page.locator(
        "form, .find_id_form, .guide_txt, input[type='text']"
    ).count() > 0
