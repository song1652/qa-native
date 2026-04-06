"""Playwright 테스트 — test_alert_simple (tc_44)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_alert_simple(page):
    """Click alert button and accept the simple alert"""
    page.goto(BASE_URL + "/alerts")
    page.wait_for_load_state("domcontentloaded")

    dialog_messages = []
    def handle_dialog(dialog):
        dialog_messages.append(dialog.message)
        dialog.accept()
    page.on("dialog", handle_dialog)

    page.locator("#alertButton").click()
    page.wait_for_timeout(2000)

    assert len(dialog_messages) > 0, "Alert dialog should have appeared"
