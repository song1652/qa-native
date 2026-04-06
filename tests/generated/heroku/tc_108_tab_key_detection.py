from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_tab_key_detection(page: Page):
    # key_presses 페이지에서 Tab 키 입력 시 감지 확인
    page.goto("https://the-internet.herokuapp.com/key_presses")
    page.wait_for_load_state("domcontentloaded")

    input_field = page.locator("#target")
    input_field.click()
    page.keyboard.press("Tab")

    expect(page.locator("#result")).to_contain_text("You entered: TAB", timeout=5000)
