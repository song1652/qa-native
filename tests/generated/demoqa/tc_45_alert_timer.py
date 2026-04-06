"""Playwright 테스트 — test_alert_timer (tc_45)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_alert_timer(page):
    """Timer alert appears after 5 seconds"""
    page.goto(BASE_URL + "/alerts")
    page.wait_for_load_state("domcontentloaded")

    dialog_messages = []
    def handle_dialog(dialog):
        dialog_messages.append(dialog.message)
        dialog.accept()
    page.on("dialog", handle_dialog)

    page.locator("#timerAlertButton").click()
    page.wait_for_timeout(7000)

    assert len(dialog_messages) > 0, "Timer alert should have appeared"
