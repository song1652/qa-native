from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_context_menu_alert_on_right_click(page: Page) -> None:
    page.goto("https://the-internet.herokuapp.com/context_menu")
    page.wait_for_load_state("domcontentloaded")

    hot_spot = page.locator("#hot-spot")
    expect(hot_spot).to_be_visible(timeout=10000)

    dialog_messages = []

    def handle_dialog(dialog):
        dialog_messages.append(dialog.message)
        dialog.accept()

    page.on("dialog", handle_dialog)
    hot_spot.click(button="right")

    page.wait_for_timeout(1000)
    assert len(dialog_messages) > 0, "Alert dialog should have appeared after right-click"
    assert "context menu" in dialog_messages[0].lower(), (
        f"Alert message should mention 'context menu', got: {dialog_messages[0]}"
    )
