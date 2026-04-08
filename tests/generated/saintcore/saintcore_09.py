import pytest
from playwright.sync_api import Page, expect

BASE_URL = "https://saintcore.kr"


def test_sale_category_shows_products(page: Page):
    page.goto(f"{BASE_URL}/category/SALE/28/")
    page.wait_for_load_state("networkidle")

    # Should be on SALE category page
    current_url = page.url
    assert "/category/" in current_url

    # Page should load with content
    assert page.title() != ""

    # Check for product list items
    product_selectors = [
        ".prdList li",
        ".goods_list li",
        ".item_list li",
        "[class*='product'] li",
    ]

    found = False
    for selector in product_selectors:
        if page.locator(selector).count() > 0:
            found = True
            break

    assert found, "No products found in SALE category"
