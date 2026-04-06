import pytest
from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"


def test_homepage_load(page: Page):
    """tc_91: Homepage Load - verify 6 category cards are displayed"""
    page.goto(BASE_URL, wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    # Verify all 6 category cards are visible
    category_texts = [
        "Elements",
        "Forms",
        "Alerts, Frame & Windows",
        "Widgets",
        "Interactions",
        "Book Store Application",
    ]

    for category in category_texts:
        card = page.locator(".card-body").filter(has_text=category)
        expect(card).to_be_visible(timeout=10000)

    # Also verify the count of category cards is 6
    cards = page.locator(".card-body h5")
    expect(cards).to_have_count(6, timeout=10000)
