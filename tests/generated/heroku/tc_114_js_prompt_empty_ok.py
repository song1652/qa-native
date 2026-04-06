from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_js_prompt_empty_ok(page: Page):
    """TC-114: JS Prompt 빈값 확인 - 텍스트 입력 없이 OK 클릭"""
    page.goto("https://the-internet.herokuapp.com/javascript_alerts")
    page.wait_for_load_state("domcontentloaded")

    def handle_dialog(dialog):
        dialog.accept("")

    page.on("dialog", handle_dialog)

    page.get_by_role("button", name="Click for JS Prompt").click()

    result = page.locator("#result")
    expect(result).to_contain_text("You entered:", timeout=10000)
