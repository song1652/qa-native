from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_disappearing_elements_nav_buttons(page: Page) -> None:
    page.goto("https://the-internet.herokuapp.com/disappearing_elements")
    page.wait_for_load_state("domcontentloaded")

    nav_items = page.locator("ul li a")
    count = nav_items.count()
    assert count >= 4, f"Expected at least 4 navigation buttons, got {count}"

    expected_labels = ["Home", "About", "Contact Us", "Portfolio"]
    visible_texts = [nav_items.nth(i).inner_text().strip() for i in range(count)]
    for label in expected_labels:
        assert label in visible_texts, f"Expected '{label}' in nav buttons, got: {visible_texts}"
