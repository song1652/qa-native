from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"

VALID_MESSAGES = ("Action successful", "Action unsuccesful")


def test_notification_message_changes_on_repeat_click(page: Page) -> None:
    page.goto("https://the-internet.herokuapp.com/notification_message")
    page.wait_for_load_state("domcontentloaded")

    page.locator("a", has_text="Click here").click()
    page.wait_for_load_state("domcontentloaded")

    flash = page.locator("#flash")
    expect(flash).to_be_visible(timeout=10000)
    first_text = flash.inner_text()

    page.locator("a", has_text="Click here").click()
    page.wait_for_load_state("domcontentloaded")

    flash2 = page.locator("#flash")
    expect(flash2).to_be_visible(timeout=10000)
    second_text = flash2.inner_text()

    assert any(msg in first_text for msg in VALID_MESSAGES), f"Unexpected first message: {first_text}"
    assert any(msg in second_text for msg in VALID_MESSAGES), f"Unexpected second message: {second_text}"
