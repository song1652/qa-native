"""Playwright 테스트 — test_menu_sub_sub_list (tc_71)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_menu_sub_sub_list(page):
    """Menu sub sub list hover"""
    page.goto(BASE_URL + "/menu")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(1000)

    # Hover Main Item 2
    main2 = page.locator("#nav > li:nth-child(2) > a")
    main2.hover()
    page.wait_for_timeout(1000)

    # Hover Sub Sub List item (3rd submenu item)
    sub_items = page.locator("#nav > li:nth-child(2) > ul > li")
    # Find the one with sub-sub items
    for i in range(sub_items.count()):
        text = sub_items.nth(i).locator("> a").inner_text().strip()
        if "SUB SUB" in text.upper():
            sub_items.nth(i).locator("> a").hover()
            break
    else:
        # Fallback: hover last sub item
        sub_items.last.locator("> a").hover()
    page.wait_for_timeout(1000)

    expect(page.locator("a:has-text('Sub Sub Item 1')")).to_be_visible(timeout=5000)
