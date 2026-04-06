from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_dynamic_controls_enable_input(page: Page):
    """Dynamic Controls 입력 필드 활성화"""
    page.goto("https://the-internet.herokuapp.com/dynamic_controls")
    page.wait_for_load_state("domcontentloaded")

    text_input = page.locator("input[type='text']")
    expect(text_input).to_be_visible(timeout=10000)
    expect(text_input).to_be_disabled(timeout=5000)

    enable_button = page.get_by_role("button", name="Enable")
    enable_button.click()

    # #loading 이 2개 존재할 수 있으므로 #message 텍스트 출현으로 대기
    message = page.locator("#message")
    expect(message).to_be_visible(timeout=15000)
    expect(message).to_contain_text("It's enabled!", timeout=10000)

    expect(text_input).to_be_enabled(timeout=10000)
