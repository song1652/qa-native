import json
from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_dynamic_loading_example2_rendered_after_start(page: Page):
    """tc_99: Dynamic Loading Example 2 렌더링 후 표시 - Start 클릭 후 DOM에 Hello World! 렌더링"""
    page.goto("https://the-internet.herokuapp.com/dynamic_loading/2")
    page.wait_for_load_state("domcontentloaded")

    start_button = page.get_by_role("button", name="Start")
    expect(start_button).to_be_visible(timeout=10000)

    start_button.click()

    # 로딩 완료 대기: #finish가 DOM에 새로 렌더링됨
    finish = page.locator("#finish")
    expect(finish).to_be_visible(timeout=15000)
    expect(finish).to_contain_text("Hello World!", timeout=10000)
