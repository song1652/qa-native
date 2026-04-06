"""Playwright 테스트 — test_alert_prompt (tc_48)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_alert_prompt(page):
    """Prompt alert accepts input"""
    page.goto(BASE_URL + "/alerts")
    page.wait_for_load_state("domcontentloaded")

    def handle_dialog(dialog):
        dialog.accept("TestUser")
    page.on("dialog", handle_dialog)

    page.locator("#promtButton").click()
    page.wait_for_timeout(1000)

    expect(page.locator("#promptResult")).to_contain_text("TestUser", timeout=5000)
