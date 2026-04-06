from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_menu_submenu_hover(page: Page):
    page.goto(f"{BASE_URL}/menu", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    main_item2 = page.get_by_text("Main Item 2", exact=True)
    expect(main_item2).to_be_visible(timeout=10000)
    main_item2.hover()
    page.wait_for_timeout(500)

    # "Sub Item" appears twice - use .first to avoid strict mode violation
    sub_item = page.get_by_text("Sub Item", exact=True).first
    expect(sub_item).to_be_visible(timeout=10000)

    # "SUB SUB LIST" text includes trailing » arrow
    sub_sub_list = page.locator("a").filter(has_text="SUB SUB LIST")
    expect(sub_sub_list).to_be_visible(timeout=10000)
