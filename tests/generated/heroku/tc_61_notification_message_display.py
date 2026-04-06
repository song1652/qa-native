from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_notification_message_display(page: Page) -> None:
    page.goto("https://the-internet.herokuapp.com/notification_message")
    page.wait_for_load_state("domcontentloaded")

    page.locator("a", has_text="Click here").click()
    page.wait_for_load_state("domcontentloaded")

    flash = page.locator("#flash")
    expect(flash).to_be_visible(timeout=10000)
    expect(flash).to_contain_text("Action", timeout=5000)
