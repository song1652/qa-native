import pytest
from playwright.sync_api import Page, expect

BASE_URL = "https://saintcore.kr"


def test_cart_page_loads(page: Page):
    page.goto(f"{BASE_URL}/")
    page.wait_for_load_state("networkidle")

    # Navigate to cart page directly
    page.goto(f"{BASE_URL}/order/basket.html")
    page.wait_for_load_state("networkidle")

    # Cart page may redirect to login if not authenticated — both are acceptable
    current_url = page.url
    assert "/order/basket" in current_url or "/member/login" in current_url

    # If actually on cart page, verify it loaded
    if "/order/basket" in current_url:
        assert page.title() != ""
