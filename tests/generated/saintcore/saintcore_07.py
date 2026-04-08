import pytest
from playwright.sync_api import Page, expect

BASE_URL = "https://saintcore.kr"


def test_main_page_shows_products(page: Page):
    page.goto(f"{BASE_URL}/")
    page.wait_for_load_state("networkidle")

    # Main page should load successfully
    assert page.title() != ""

    # Products should be visible - check common product list containers
    product_selectors = [
        ".prdList li",
        ".goods_list li",
        ".item_list li",
        "[class*='product'] li",
        ".main_prd li",
    ]

    found = False
    for selector in product_selectors:
        if page.locator(selector).count() > 0:
            found = True
            break

    assert found, "No product items found on main page"
