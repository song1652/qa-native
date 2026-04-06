from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_key_press_detection(page: Page):
    """키 입력 감지"""
    page.goto("https://the-internet.herokuapp.com/key_presses")
    page.wait_for_load_state("domcontentloaded")

    # Enter 키가 폼 제출 트리거가 되지 않도록 form submit preventDefault 처리
    page.evaluate("""
        () => {
            const form = document.querySelector('form');
            if (form) {
                form.addEventListener('submit', (e) => e.preventDefault());
            }
        }
    """)

    text_input = page.locator("#target")
    expect(text_input).to_be_visible(timeout=10000)
    text_input.click()
    text_input.press("A")

    result = page.locator("#result")
    expect(result).to_contain_text("You entered: A", timeout=5000)
