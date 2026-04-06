from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_js_alert_text_verify(page: Page):
    """TC-115: JS Alert 텍스트 확인 - Alert 메시지 확인 후 OK 클릭"""
    page.goto("https://the-internet.herokuapp.com/javascript_alerts")
    page.wait_for_load_state("domcontentloaded")

    captured = {}

    def handle_dialog(dialog):
        captured["message"] = dialog.message
        dialog.accept()

    page.on("dialog", handle_dialog)

    page.get_by_role("button", name="Click for JS Alert").click()

    result = page.locator("#result")
    expect(result).to_contain_text("You successfully clicked an alert", timeout=10000)

    assert captured.get("message") == "I am a JS Alert", (
        f"Expected alert message 'I am a JS Alert', got: {captured.get('message')}"
    )
