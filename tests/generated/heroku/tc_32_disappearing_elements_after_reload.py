from pathlib import Path
from playwright.sync_api import Page

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_disappearing_elements_after_reload(page: Page) -> None:
    page.goto("https://the-internet.herokuapp.com/disappearing_elements")
    page.wait_for_load_state("domcontentloaded")

    nav_items = page.locator("ul li a")
    before_count = nav_items.count()
    assert before_count >= 4, f"Expected at least 4 nav buttons before reload, got {before_count}"

    page.reload()
    page.wait_for_load_state("domcontentloaded")

    nav_items_after = page.locator("ul li a")
    after_count = nav_items_after.count()
    assert after_count >= 4, f"Expected at least 4 nav buttons after reload, got {after_count}"
