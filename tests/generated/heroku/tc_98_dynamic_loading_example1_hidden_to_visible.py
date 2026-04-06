import json
from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_dynamic_loading_example1_hidden_to_visible(page: Page):
    """tc_98: Dynamic Loading Example 1 숨김에서 표시 - Start 클릭 후 Hello World! 텍스트 표시"""
    page.goto("https://the-internet.herokuapp.com/dynamic_loading/1")
    page.wait_for_load_state("domcontentloaded")

    start_button = page.get_by_role("button", name="Start")
    expect(start_button).to_be_visible(timeout=10000)

    start_button.click()

    # 로딩 완료 대기: #loading이 사라지고 #finish가 표시됨
    finish = page.locator("#finish")
    expect(finish).to_be_visible(timeout=15000)
    expect(finish).to_contain_text("Hello World!", timeout=10000)
