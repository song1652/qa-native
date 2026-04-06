import json
from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_enter_key_detection(page: Page):
    # key_presses 페이지에서 Enter 키 입력 시 감지 확인
    page.goto("https://the-internet.herokuapp.com/key_presses")
    page.wait_for_load_state("domcontentloaded")

    # form submit 이벤트 preventDefault (Enter가 폼 제출 트리거 방지)
    page.evaluate("""
        () => {
            const form = document.querySelector('form');
            if (form) {
                form.addEventListener('submit', e => e.preventDefault());
            }
        }
    """)

    input_field = page.locator("#target")
    input_field.click()
    page.keyboard.press("Enter")

    expect(page.locator("#result")).to_contain_text("You entered: ENTER", timeout=5000)
