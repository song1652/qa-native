from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_menu_sub_sub_list(page: Page):
    page.goto(f"{BASE_URL}/menu", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    main_item2 = page.get_by_text("Main Item 2", exact=True)
    expect(main_item2).to_be_visible(timeout=10000)
    main_item2.hover()
    page.wait_for_timeout(500)

    # "SUB SUB LIST" text may include trailing » arrow - use filter
    sub_sub_list = page.locator("a").filter(has_text="SUB SUB LIST")
    expect(sub_sub_list).to_be_visible(timeout=10000)
    sub_sub_list.hover()
    page.wait_for_timeout(500)

    sub_sub_item1 = page.get_by_text("Sub Sub Item 1", exact=True)
    sub_sub_item2 = page.get_by_text("Sub Sub Item 2", exact=True)

    expect(sub_sub_item1).to_be_visible(timeout=10000)
    expect(sub_sub_item2).to_be_visible(timeout=10000)
